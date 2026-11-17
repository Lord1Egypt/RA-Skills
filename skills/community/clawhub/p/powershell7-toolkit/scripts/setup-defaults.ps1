#Requires -Version 5.1
<#
.SYNOPSIS
    把 pwsh 配置为系统默认，并根治中文乱码。所有改动均为【用户级】，不需要管理员权限，可一键回退。
.PARAMETER PwshPath
    pwsh.exe 的完整路径。不填则自动探测系统里已安装的 PowerShell 7。
.PARAMETER BinDir
    Rust 工具目录（rg/fd/fzf/bat/delta/jq）。不填则用 $env:LOCALAPPDATA\ps7-toolkit\bin
.PARAMETER ToolsRoot
    安装根目录（仅用于推导默认路径）
#>
[CmdletBinding()]
param(
    [string]$PwshPath,
    [string]$BinDir,
    [string]$ToolsRoot = (Join-Path $env:LOCALAPPDATA 'ps7-toolkit')
)

$ErrorActionPreference = 'Continue'

# ---- 自动探测 pwsh ----
if (-not $PwshPath) {
    $cands = @(
        (Join-Path $ToolsRoot 'ps7\pwsh.exe'),
        'C:\Program Files\PowerShell\7\pwsh.exe',
        'C:\Program Files\PowerShell\7-preview\pwsh.exe',
        (Join-Path $env:LOCALAPPDATA 'Programs\PowerShell\7\pwsh.exe'),
        (Join-Path $env:USERPROFILE 'scoop\apps\powershell\current\pwsh.exe')
    )
    $g = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($g) { $cands += $g.Source }
    foreach ($k in @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe',
                     'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe')) {
        if (Test-Path $k) { $v = (Get-ItemProperty $k -ErrorAction SilentlyContinue).'(default)'; if ($v) { $cands += $v } }
    }
    foreach ($c in ($cands | Where-Object { $_ } | Select-Object -Unique)) {
        if (Test-Path $c) { $PwshPath = $c; break }
    }
}
if (-not $PwshPath) { Write-Host "    [X] 找不到 pwsh.exe，跳过默认化" -ForegroundColor Red; exit 1 }

# 没显式传 -ToolsRoot 时，优先从探测到的 pwsh 反推根目录：<root>\ps7\pwsh.exe -> <root>
# 否则会出现错位：PS7Dir 是从 $PwshPath 反推的（G:\Tools\ps7，对），
# BinDir 却从写死的 $ToolsRoot 拼（%LOCALAPPDATA%\ps7-toolkit\bin，根本不存在），
# 于是独立运行本脚本时往 PATH 里加一条死链。install.ps1 会显式传 -BinDir，只有独立运行会中招。
if (-not $PSBoundParameters.ContainsKey('ToolsRoot')) {
    $pwshDir = Split-Path -Parent $PwshPath
    $maybeRoot = Split-Path -Parent $pwshDir
    if ($maybeRoot -and (Test-Path (Join-Path $maybeRoot 'ps7\pwsh.exe'))) { $ToolsRoot = $maybeRoot }
}

$PS7Dir = Split-Path -Parent $PwshPath
if (-not $BinDir) { $BinDir = Join-Path $ToolsRoot 'bin' }

function Say ($m) { Write-Host $m }

# ---------------------------------------------------------------- 1. profile（UTF-8 根治）
Say "`n[1/6] 写入 PowerShell profile（强制 UTF-8）"
$docs = [Environment]::GetFolderPath('MyDocuments')
$profiles = @{
    (Join-Path $docs 'WindowsPowerShell\Microsoft.PowerShell_profile.ps1') = 'PS5.1'
    (Join-Path $docs 'PowerShell\Microsoft.PowerShell_profile.ps1')          = 'PS7'
}
foreach ($p in $profiles.Keys) {
    $dir = Split-Path -Parent $p
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    $extra = ''
    if ($profiles[$p] -eq 'PS7') {
        $extra = "`r`n# Rust high-performance tools (rg/fd/fzf/bat/delta/jq)`r`nif (`$env:PATH -notlike ('*' + '$BinDir' + '*')) { `$env:PATH = '$BinDir;' + `$env:PATH }"
    }
    $content = @"
# ===== ps7-toolkit: force UTF-8 everywhere =====
# Fixes garbled Chinese output for every app that shells out to PowerShell.
try {
    `$utf8 = New-Object System.Text.UTF8Encoding `$false
    [Console]::OutputEncoding = `$utf8
    `$global:OutputEncoding = `$utf8
    `$PSDefaultParameterValues['Out-File:Encoding']    = 'utf8'
    `$PSDefaultParameterValues['Set-Content:Encoding'] = 'utf8'
    `$PSDefaultParameterValues['Add-Content:Encoding'] = 'utf8'
} catch { }
$extra
"@
    if ((Test-Path $p) -and ((Get-Content $p -Raw -ErrorAction SilentlyContinue) -match 'ps7-toolkit')) {
        Say "    已存在(跳过): $p"
    } else {
        if (Test-Path $p) { Copy-Item $p "$p.bak" -Force }
        [System.IO.File]::WriteAllText($p, $content, (New-Object System.Text.UTF8Encoding $true))
        Say "    已写入: $p"
    }
}

# ---------------------------------------------------------------- 2. 用户 PATH
Say "`n[2/6] 配置用户 PATH"
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if (-not $userPath) { $userPath = '' }

# 逐项处理，不用 -like "*$d*" 那种子串包含：
#   1) 子串匹配会让 G:\Tools\bin2 因为「含 G:\Tools\bin」而被跳过（其实没配）；
#   2) 老逻辑只做「缺了就追加」，换安装目录重装后旧 root 的项永远留着，最后变成死链。
$entries = @()
foreach ($e in $userPath.Split(';')) {
    $t = $e.Trim()
    if ($t) { $entries += $t }
}

$kept = @(); $pruned = @()
foreach ($e in $entries) {
    $exp = [Environment]::ExpandEnvironmentVariables($e).TrimEnd('\')
    # 只清理「看起来是本工具装的、且目录确实已经不在了」的项；别人的路径一律不动
    $ours = ($exp -match 'ps7-toolkit') -or ($exp -eq $PS7Dir.TrimEnd('\')) -or ($exp -eq $BinDir.TrimEnd('\'))
    # 再退一步：连所在的盘都不可用（移动硬盘没插、网络盘断线）就不动，免得拔一次盘配置就被删了
    $rootUsable = $true
    try {
        $root = [System.IO.Path]::GetPathRoot($exp)
        if ($root) { $rootUsable = Test-Path $root }
    } catch { }
    if ($ours -and $rootUsable -and -not (Test-Path $exp)) { $pruned += $e } else { $kept += $e }
}

$add = @()
foreach ($d in @($PS7Dir, $BinDir)) {
    # 只加真实存在的目录：否则上一段刚清掉的死链，这一段又原样加回来（左手删右手加）
    if (-not (Test-Path $d)) { Say "    [!] 目录不存在，跳过: $d"; continue }
    $dn = $d.TrimEnd('\')
    $has = $false
    foreach ($e in $kept) {
        if ([string]::Equals($e.TrimEnd('\'), $dn, [StringComparison]::OrdinalIgnoreCase)) { $has = $true; break }
    }
    if (-not $has) { $add += $d }
}

$pathChanged = $false
if ($add.Count -gt 0 -or $pruned.Count -gt 0) {
    [Environment]::SetEnvironmentVariable('Path', ((@($kept) + @($add)) -join ';'), 'User')
    $pathChanged = $true
    if ($pruned.Count -gt 0) { Say "    已移除失效的旧路径: $($pruned -join ', ')" }
    if ($add.Count -gt 0) { Say "    已加入: $($add -join ', ')" }
} else { Say "    PATH 已包含，无需修改" }

# 旧工具目录并存提示（升级场景常见：旧安装的 bin 与新 bin 同时在 PATH，内容相同、不冲突）。
# 按设计绝不删用户自己的目录，只打印一行让用户知道可以手动清理。
$oldTools = @()
foreach ($e in $kept) {
    $exp = [Environment]::ExpandEnvironmentVariables($e).TrimEnd('\')
    if ([string]::Equals($exp, $PS7Dir.TrimEnd('\'), [StringComparison]::OrdinalIgnoreCase)) { continue }
    if ([string]::Equals($exp, $BinDir.TrimEnd('\'),  [StringComparison]::OrdinalIgnoreCase)) { continue }
    if ((Test-Path (Join-Path $exp 'rg.exe')) -or (Test-Path (Join-Path $exp 'fd.exe'))) { $oldTools += $exp }
}
if ($oldTools.Count -gt 0) {
    Say "    [!] 检测到旧工具目录仍在 PATH（与本包新目录并存）: $($oldTools -join ', ')"
    Say "        功能不冲突。如确认不再需要，可手动从用户 PATH 中移除。"
}

# ---------------------------------------------------------------- 3. App Paths
Say "`n[3/6] 注册 App Paths\pwsh.exe"
$k = 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe'
if (-not (Test-Path $k)) { New-Item -Path $k -Force | Out-Null }
Set-ItemProperty -Path $k -Name '(default)' -Value $PwshPath -ErrorAction SilentlyContinue
Set-ItemProperty -Path $k -Name 'Path' -Value $PS7Dir -ErrorAction SilentlyContinue
Say "    $PwshPath"

# ---------------------------------------------------------------- 4. .ps1 文件关联
Say "`n[4/6] 设置 .ps1 文件关联 -> pwsh"
$cmd = "`"$PwshPath`" -NoLogo -NoProfile -File `"%1`""
$k2 = 'HKCU:\Software\Microsoft\Classes\.ps1\shell\open\command'
if (-not (Test-Path $k2)) { New-Item -Path $k2 -Force | Out-Null }
Set-ItemProperty -Path $k2 -Name '(default)' -Value $cmd
Say "    $cmd"
Say "    (提示: 双击 .ps1 会直接执行脚本。想撤销: 删除 HKCU:\Software\Microsoft\Classes\.ps1)"

# ---------------------------------------------------------------- 5. 开始菜单入口
Say "`n[5/6] 开始菜单入口"
$menu = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'
$lnk = Join-Path $menu 'PowerShell 7.lnk'
$entry = Join-Path $menu 'PowerShell 7.cmd'

# 为什么不再建 .lnk：创建 .lnk 只有两条路 —— 调用系统 COM 组件或运行时编译，
# 这两条路在部分 AI 客户端里都会被工具层安全规则直接拦住，而且一拦就是整段脚本失败。
# 这里不再做「先试 COM 再兜底」的写法，因为尝试本身就会触发拦截；
# 直接用 .cmd 入口，双击行为、开始菜单搜索效果都一致。
if (Test-Path $lnk) {
    Say "    已存在快捷方式: PowerShell 7.lnk，保持不变"
} else {
    $body = "@echo off`r`nstart `"`" `"$PwshPath`" %*`r`n"
    $enc = $null
    try { $enc = [System.Text.Encoding]::GetEncoding(936) }
    catch { $enc = New-Object System.Text.UTF8Encoding $false }
    try {
        [System.IO.File]::WriteAllText($entry, $body, $enc)
        Say "    已创建开始菜单入口: PowerShell 7.cmd"
        Say "    (说明: 受限环境不建 .lnk，用 .cmd 等价入口；开始菜单搜索里同样能搜到)"
    } catch { Say "    [!] 创建开始菜单入口失败: $($_.Exception.Message)" }
}

# ---------------------------------------------------------------- 6. Windows Terminal / VSCode
Say "`n[6/6] 配置 Windows Terminal 与 VSCode"

# 配置文件的改写逻辑放在 wt-config.ps1 里（可被回归测试单独测），这里只负责调用。
$helper = Join-Path $PSScriptRoot 'wt-config.ps1'
if (Test-Path $helper) { . $helper }
else { Say "    [!] 缺少 wt-config.ps1（应与本脚本同目录），跳过 WT/VSCode 配置" }

$wtPkg = Join-Path $env:LOCALAPPDATA 'Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe'

# ---- 6a. 默认终端程序 ----
# 真正的开关是 HKCU\Console\%%Startup 的两个 GUID 值（微软官方文档口径）。
# 以前写的是 Explorer\Advanced 下的 DelegationConsole —— 那个位置系统根本不读，等于什么都没做，
# 体检那边也只查「键是否存在」，所以一直是假 OK。
# 这一段必须独立于下面的 settings.json 解析：那一步可能因为 JSONC 语法失败，
# 但不能连带把默认终端一起跳过（用户只会看到一句「WT 配置失败」，根本不知道少设了一项）。
if (Test-Path $wtPkg) {
    try {
        $startup = 'HKCU:\Console\%%Startup'
        if (-not (Test-Path $startup)) { New-Item -Path $startup -Force | Out-Null }
        Set-ItemProperty -Path $startup -Name 'DelegationConsole'  -Value '{2EACA947-7F5F-4CFA-BA87-8F7FBEEFBE69}'
        Set-ItemProperty -Path $startup -Name 'DelegationTerminal' -Value '{E12CFF52-A866-4C77-9A90-F570A7AA2C6B}'
        Say "    默认终端程序 -> Windows Terminal"
    } catch { Say "    默认终端程序设置失败: $($_.Exception.Message)" }
} else { Say "    未检测到 Windows Terminal，跳过默认终端设置" }

# ---- 6b. WT 的 profile 与 defaultProfile ----
# settings.json 是 JSONC（默认带 // 注释），不能 ConvertFrom-Json 后整文件重写：
# 那样一遇到注释就抛错，而且重写会把用户的注释、空行、字段顺序全抹掉。
if ((Test-Path $wtPkg) -and (Get-Command Update-WtSettings -ErrorAction SilentlyContinue)) {
    $wt = Join-Path $wtPkg 'LocalState\settings.json'
    if (Test-Path $wt) {
        try {
            $r = Update-WtSettings -Path $wt -PwshPath $PwshPath
            if ($r.Changed) {
                Say "    Windows Terminal: 默认配置 -> PowerShell 7（在原文件上定点修改，注释保留）"
                if ($r.Backup) { Say "    原文件已备份: $($r.Backup)" }
            } else { Say "    Windows Terminal: 已经是 PowerShell 7，无需修改" }
        } catch { Say "    Windows Terminal 配置失败: $($_.Exception.Message)" }
    } else { Say "    未检测到 Windows Terminal 配置，跳过" }
}

# ---- 6c. VSCode ----
# VSCode 的 settings.json 同样是 JSONC，而且用户自建的 profile（Ubuntu/WSL 等）要保住，
# 所以只改「PowerShell 7」这一条，不再整对象替换。
$vs = Join-Path $env:APPDATA 'Code\User\settings.json'
if ((Test-Path $vs) -and (Get-Command Update-VsCodeSettings -ErrorAction SilentlyContinue)) {
    try {
        $rv = Update-VsCodeSettings -Path $vs -PwshPath $PwshPath
        if ($rv.Changed) {
            Say "    VSCode 默认终端 -> PowerShell 7"
            if ($rv.Backup) { Say "    原文件已备份: $($rv.Backup)" }
        } else { Say "    VSCode 已经是 PowerShell 7，无需修改" }
    } catch { Say "    VSCode 配置失败: $($_.Exception.Message)" }
} else { Say "    未检测到 VSCode，跳过" }

# 环境变量广播的说明：
#   5.1 下 [Environment]::SetEnvironmentVariable(...,'User') 内部会自己发 WM_SETTINGCHANGE，
#   新开的应用能立刻读到新 PATH，不需要额外动作。
#   pwsh 7 的 .NET 实现不发广播，以前这里用运行时编译去调系统的环境广播接口补这一刀，
#   但那条路在受限环境会被工具层拦住（而且被 catch 静默吞掉），用户只会觉得「装了没生效」。
#   现在不做运行时编译，改成如实告知：需要用户自己重登或重启资源管理器。
if ($pathChanged) {
    if ($PSVersionTable.PSEdition -eq 'Core') {
        Say "`n    [!] 用户 PATH 已更新，但 pwsh 7 不会自动广播变更。"
        Say "        请注销重登，或在任务管理器里重启「Windows 资源管理器」，新开的终端才能读到新 PATH。"
    } else {
        Say "`n    环境变量变更已广播（新开的应用立即生效）"
    }
}
Say "`n默认化完成。`n"
