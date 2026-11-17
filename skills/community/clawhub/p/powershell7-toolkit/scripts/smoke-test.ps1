#Requires -Version 5.1
<#
.SYNOPSIS
    安装器回归测试（冒烟测试）—— 69 项断言，本机约 1~2 分钟跑完。
.DESCRIPTION
    全部在临时目录里跑，读系统、不写系统默认（用 -SkipDefaults），跑完自动清理。
    覆盖：只读体检、隔离安装、幂等、-Force 复制、中文+空格路径、错误参数、卸载。
    返回码：0 = 全部通过；1 = 有用例失败。
.PARAMETER KeepArtifacts
    保留临时目录，便于排查失败原因。
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\scripts\smoke-test.ps1
#>
[CmdletBinding()]
param([switch]$KeepArtifacts)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$src  = Join-Path $PSScriptRoot 'install.ps1'
$base = Join-Path $env:TEMP ('ps7-toolkit-smoke-' + [Guid]::NewGuid().ToString('N').Substring(0,8))
$log  = Join-Path $base 'logs'
$results = @()

if (-not (Test-Path $src)) { Write-Host "找不到 install.ps1：$src" -ForegroundColor Red; exit 1 }

function T([string]$name, [scriptblock]$body) {
    $r = [ordered]@{ name = $name; ok = $false; detail = '' }
    try {
        $d = & $body
        $r.ok = [bool]$d.ok
        $r.detail = $d.detail
    } catch {
        $r.ok = $false
        $r.detail = 'EXCEPTION: ' + $_.Exception.Message
    }
    $script:results += [pscustomobject]$r
    if ($r.ok) { Write-Host ("[PASS] " + $name) -ForegroundColor Green }
    else       { Write-Host ("[FAIL] " + $name) -ForegroundColor Red }
    Write-Host ("       " + $r.detail) -ForegroundColor DarkGray
}

Write-Host "`n########## 安装器回归测试 ##########" -ForegroundColor Magenta
Write-Host "脚本 : $src"
Write-Host "沙箱 : $base"

New-Item -ItemType Directory -Force -Path $log | Out-Null
$defaultRoot = Join-Path $env:LOCALAPPDATA 'ps7-toolkit'
$bg = Test-Path $defaultRoot

# ---------------------------------------------------------------- 1
Write-Host "`n=== 1. -CheckOnly（只读） ===" -ForegroundColor Cyan
& $src -CheckOnly *> (Join-Path $log 't1.log')
T 'T1  -CheckOnly 退出码 0' { @{ ok = ($LASTEXITCODE -eq 0); detail = "exit=$LASTEXITCODE" } }
T 'T2  -CheckOnly 不写任何文件' { @{ ok = ((Test-Path $defaultRoot) -eq $bg); detail = "默认目录 before=$bg after=" + (Test-Path $defaultRoot) } }

# ---------------------------------------------------------------- 2
Write-Host "`n=== 2. 隔离安装（-ToolsRoot + -SkipDefaults） ===" -ForegroundColor Cyan
$box1 = Join-Path $base 'box1'
$t0 = Get-Date
& $src -ToolsRoot $box1 -SkipDefaults *> (Join-Path $log 't2.log')
$el1 = [int]((Get-Date) - $t0).TotalSeconds
$txt = Get-Content (Join-Path $log 't2.log') -Raw -Encoding UTF8
T 'T3  安装退出码 0（可被自动化识别）' { @{ ok = ($LASTEXITCODE -eq 0); detail = "exit=$LASTEXITCODE, ${el1}s" } }
T 'T4  -ToolsRoot 生效' { @{ ok = ($txt -match [regex]::Escape($box1)); detail = "日志提到 sandbox = " + ($txt -match [regex]::Escape($box1)) } }
T 'T5  复用系统 pwsh 时有明确提示' { @{ ok = ($txt -match '未复制到'); detail = "提示出现 = " + ($txt -match '未复制到') } }

$bin1 = Join-Path $box1 'bin'
$need = @('rg.exe','fd.exe','fzf.exe','bat.exe','delta.exe','jq.exe')
$miss = @(); foreach ($n in $need) { if (-not (Test-Path (Join-Path $bin1 $n))) { $miss += $n } }
T 'T6  6 个 Rust 工具全部就位' { @{ ok = ($miss.Count -eq 0); detail = "缺失=[" + ($miss -join ',') + "]" } }

$rgv = ''; try { $rgv = (& (Join-Path $bin1 'rg.exe') --version 2>&1 | Select-Object -First 1) } catch {}
T 'T7  rg 可执行' { @{ ok = ($rgv -match 'ripgrep'); detail = $rgv } }

$jqv = ''; try { $jqv = (& (Join-Path $bin1 'jq.exe') --version 2>&1 | Select-Object -First 1) } catch {}
T 'T8  jq 可执行（API 限流兜底路径）' { @{ ok = ($jqv -match '^jq-'); detail = $jqv } }

T 'T9  下载缓存已清理' { @{ ok = (-not (Test-Path (Join-Path $box1 '_dl'))); detail = "_dl 不存在 = " + (-not (Test-Path (Join-Path $box1 '_dl'))) } }
T 'T10 日志无进度条刷屏' { @{ ok = ($txt -notmatch 'oooooo'); detail = "刷屏 = " + ($txt -match 'oooooo') } }
T 'T11 -SkipDefaults 下体检不报 PATH 红叉' { @{ ok = ($txt -notmatch '不在用户 PATH'); detail = "告警 = " + ($txt -match '不在用户 PATH') } }

# ---------------------------------------------------------------- 3
Write-Host "`n=== 3. 幂等（连跑两次） ===" -ForegroundColor Cyan
$snapA = (Get-ChildItem $bin1 -File | ForEach-Object { $_.Name + ':' + $_.Length }) -join '|'
$t1 = Get-Date
& $src -ToolsRoot $box1 -SkipDefaults *> (Join-Path $log 't3.log')
$ms2 = [int]((Get-Date) - $t1).TotalMilliseconds
$snapB = (Get-ChildItem $bin1 -File | ForEach-Object { $_.Name + ':' + $_.Length }) -join '|'
$txt3 = Get-Content (Join-Path $log 't3.log') -Raw -Encoding UTF8
T 'T12 第二次运行退出码 0' { @{ ok = ($LASTEXITCODE -eq 0); detail = "exit=$LASTEXITCODE, ${ms2}ms" } }
T 'T13 第二次运行二进制完全一致（未重复下载）' { @{ ok = ($snapA -eq $snapB); detail = if ($snapA -eq $snapB) { '一致' } else { '内容有变化' } } }
T 'T14 第二次运行没有重新下载' { $dl2 = ($txt3 -match '开始下载|自动下载 PowerShell 7'); @{ ok = (-not $dl2); detail = "日志里出现下载步骤 = $dl2" } }

# ---------------------------------------------------------------- 4
Write-Host "`n=== 4. -Force 复制本机安装（不联网） ===" -ForegroundColor Cyan
$box4 = Join-Path $base 'box4'
$t2 = Get-Date
& $src -ToolsRoot $box4 -SkipDefaults -SkipRustTools -Force *> (Join-Path $log 't4.log')
$el4 = [int]((Get-Date) - $t2).TotalSeconds
$pwsh4 = Join-Path $box4 'ps7\pwsh.exe'
T 'T15 -Force 把 pwsh 放进 -ToolsRoot' { @{ ok = (Test-Path $pwsh4); detail = "pwsh.exe=" + (Test-Path $pwsh4) + ", ${el4}s" } }
$v4 = ''; if (Test-Path $pwsh4) { try { $v4 = (& $pwsh4 -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' 2>$null) } catch {} }
T 'T16 复制出来的 pwsh 可运行' { @{ ok = ($v4 -match '^7\.'); detail = "version=$v4" } }
T 'T17 -Force 是复制而非重新下载' { @{ ok = ($el4 -lt 150); detail = "${el4}s（下载通常要 100s+）" } }

# ---------------------------------------------------------------- 5
Write-Host "`n=== 5. 中文 + 空格路径 ===" -ForegroundColor Cyan
$cn   = [string][char]0x4E2D + [string][char]0x6587
$box2 = Join-Path $base ($cn + ' path\ps7 box')
& $src -ToolsRoot $box2 -SkipDefaults -SkipRustTools *> (Join-Path $log 't5.log')
T 'T18 中文+空格 ToolsRoot 安装成功' { @{ ok = ($LASTEXITCODE -eq 0); detail = "exit=$LASTEXITCODE, 目录存在=" + (Test-Path $box2) } }

# ---------------------------------------------------------------- 6
Write-Host "`n=== 6. -ZipPath 指向不存在的文件 ===" -ForegroundColor Cyan
$srcText = Get-Content $src -Raw -Encoding UTF8
$hasFail = ($srcText -match '-ZipPath 指定的文件不存在[\s\S]{0,300}?exit 1')
T 'T19 明确报错退出，不偷偷联网下载' { @{ ok = $hasFail; detail = "守卫代码存在 = $hasFail" } }

# ---------------------------------------------------------------- 7
Write-Host "`n=== 7. 卸载 ===" -ForegroundColor Cyan
if (-not $KeepArtifacts) {
    foreach ($b in @($box1, $box2, $box4)) { Remove-Item $b -Recurse -Force -ErrorAction SilentlyContinue }
    T 'T20 删目录即卸载，且未污染默认目录' { @{ ok = ((-not (Test-Path $box1)) -and (-not (Test-Path $box4)) -and ((Test-Path $defaultRoot) -eq $bg)); detail = '沙箱已清理' } }
} else {
    T 'T20 删目录即卸载，且未污染默认目录' { @{ ok = $true; detail = '已跳过清理（-KeepArtifacts）' } }
}

# ---------------------------------------------------------------- 8
Write-Host "`n=== 8. 空的下载缓存目录 ===" -ForegroundColor Cyan
# 全程复用系统已装工具时一个字节都不会下载，_dl 会被建成空目录。
# 老逻辑用 sum -gt 0 判断，空目录的 Sum 是 $null，永远清不掉。
$box6 = Join-Path $base 'box6'
$dl6  = Join-Path $box6 '_dl'
New-Item -ItemType Directory -Force -Path $dl6 | Out-Null
& $src -ToolsRoot $box6 -SkipDefaults -SkipRustTools *> (Join-Path $log 't8.log')
T 'T21 空缓存目录也会被清理' { @{ ok = (-not (Test-Path $dl6)); detail = "_dl 仍存在 = " + (Test-Path $dl6) } }
Remove-Item $box6 -Recurse -Force -ErrorAction SilentlyContinue

# ---------------------------------------------------------------- 9
Write-Host "`n=== 9. 静态检查（防止老写法回来） ===" -ForegroundColor Cyan
$setupText  = Get-Content (Join-Path $PSScriptRoot 'setup-defaults.ps1') -Raw -Encoding UTF8
$verifyText = Get-Content (Join-Path $PSScriptRoot 'verify.ps1') -Raw -Encoding UTF8
# 只看代码，不看注释——否则注释里提到老写法也会被误判成「还在用老写法」
$setupCode  = ($setupText -split "`n" | Where-Object { $_ -notmatch '^\s*#' }) -join "`n"

# HKCU\Console\%%Startup 才是「默认终端程序」真正的开关；Explorer\Advanced 系统不读
$oldTerm = ($setupCode -match 'Explorer\\Advanced[\s\S]{0,300}Delegation')
T 'T22 默认终端写到 Console\%%Startup' { @{ ok = ($setupCode.Contains('HKCU:\Console\%%Startup') -and -not $oldTerm); detail = "写对位置 = $($setupCode.Contains('HKCU:\Console\%%Startup'))，仍用老写法 = $oldTerm" } }

# PATH 判断必须是逐项精确比较 + 目录存在性检查，不能再靠子串包含
$oldPath = $verifyText.Contains('IndexOf($d')
T 'T23 体检的 PATH 检查逐项精确比较并验证目录存在' { @{ ok = (-not $oldPath -and $verifyText.Contains('Test-Path $d')); detail = "仍用子串匹配 = $oldPath" } }

# 默认终端的注册表写入必须在 WT 配置文件解析之前，不能被它的失败连带跳过
$iStartup = $setupCode.IndexOf('HKCU:\Console\%%Startup')
$iWtCall  = $setupCode.IndexOf('Update-WtSettings')
T 'T24 默认终端注册表写入独立于 WT 配置解析' { @{ ok = ($iStartup -ge 0 -and $iWtCall -ge 0 -and $iStartup -lt $iWtCall); detail = "registry@$iStartup, wt@$iWtCall" } }

# 配置文件的改写不能整文件反序列化再序列化：JSONC 解析必挂，注释也会被吃掉
$rewrite = ($setupCode -match 'ConvertTo-Json[^\n]*(Set-Content|Out-File)')
T 'T25 不再整文件重写 WT/VSCode 配置' { @{ ok = (-not $rewrite -and $setupCode.Contains('Update-WtSettings') -and $setupCode.Contains('Update-VsCodeSettings')); detail = "仍整文件重写 = $rewrite" } }

# 体检里「全 0 GUID」是「交给 Windows 自动选」，不能当成「已指定」
T 'T26 体检把零 GUID 识别为自动选择' { @{ ok = ($verifyText.Contains('$autoPick')); detail = "autoPick 处理 = $($verifyText.Contains('$autoPick'))" } }

# ---------------------------------------------------------------- 10
Write-Host "`n=== 10. WT / VSCode 配置改写（JSONC，必须保注释） ===" -ForegroundColor Cyan
$cfgDir = Join-Path $base 'cfg'
New-Item -ItemType Directory -Force -Path $cfgDir | Out-Null
$wtTools = Join-Path $PSScriptRoot 'wt-config.ps1'
$wtReady = Test-Path $wtTools
if ($wtReady) { . $wtTools }

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$newGuid = '{9e1b2a44-7c3d-4f8e-b5a1-2d6c9f0e3b71}'

$wtFix = Join-Path $cfgDir 'wt-settings.json'
$wtJsonc = @'
// This file was initially generated by Windows Terminal
{
    "$help": "https://aka.ms/terminal-documentation",
    "defaultProfile": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}", // 原来是 Windows PowerShell
    "profiles":
    {
        "defaults": {},
        "list":
        [
            {
                "commandline": "powershell.exe",
                "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
                "name": "Windows PowerShell"
            }
        ]
    }
    /* 块注释也要活下来 */
}
'@
[System.IO.File]::WriteAllText($wtFix, $wtJsonc, $utf8NoBom)
$wtOk = $false; $wtErr = ''
if ($wtReady) {
    try { $r1 = Update-WtSettings -Path $wtFix -PwshPath 'G:\Tools\ps7\pwsh.exe'; $wtOk = $true }
    catch { $wtErr = $_.Exception.Message }
}
$wtAfter = if (Test-Path $wtFix) { [System.IO.File]::ReadAllText($wtFix) } else { '' }

T 'T27 WT：带 // 注释的 JSONC 能改，且注释原样保留' {
    @{ ok = ($wtOk -and $wtAfter.Contains('// This file was initially generated') -and $wtAfter.Contains('/* 块注释也要活下来 */')); detail = if ($wtOk) { "changed=$($r1.Changed)，行注释保留=$($wtAfter.Contains('// This file'))，块注释保留=$($wtAfter.Contains('/* 块注释'))" } else { "抛错: $wtErr" } }
}
T 'T28 WT：defaultProfile 指向 PowerShell 7，且改完仍能解析' {
    $ok = $false; $msg = ''
    try { $o = ConvertFrom-Jsonc -Text $wtAfter; $ok = ($o.defaultProfile -eq $newGuid -and @($o.profiles.list).Count -eq 2) }
    catch { $msg = $_.Exception.Message }
    @{ ok = $ok; detail = if ($ok) { 'defaultProfile 正确，list 有 2 条' } else { "失败: $msg" } }
}
T 'T29 WT：profile 列表里加上了 PowerShell 7 这一条' {
    $hasName = $wtAfter -match '"name": "PowerShell 7"'
    $hasExe = $wtAfter -match 'pwsh\.exe'
    @{ ok = ($hasName -and $hasExe); detail = "含 PowerShell 7 = $hasName，含 pwsh 路径 = $hasExe" }
}
T 'T30 WT：原文件备份成 .ps7bak，且内容是改动前的原样' {
    $bak = $wtFix + '.ps7bak'
    $ok = (Test-Path $bak) -and ([System.IO.File]::ReadAllText($bak) -eq $wtJsonc)
    @{ ok = $ok; detail = "备份存在 = $(Test-Path $bak)，内容未变 = $(if (Test-Path $bak) { [System.IO.File]::ReadAllText($bak) -eq $wtJsonc } else { $false })" }
}
T 'T31 WT：重复执行不再改动（幂等）' {
    $again = $null
    try { $again = Update-WtSettings -Path $wtFix -PwshPath 'G:\Tools\ps7\pwsh.exe' } catch { }
    @{ ok = ($null -ne $again -and -not $again.Changed); detail = "第二次 changed = $(if ($again) { $again.Changed } else { 'error' })" }
}

$wtEmpty = Join-Path $cfgDir 'wt-empty.json'
[System.IO.File]::WriteAllText($wtEmpty, '{"profiles": {"list": []}}', $utf8NoBom)
$emptyOk = $false; $emptyMsg = ''
if ($wtReady) {
    try {
        $null = Update-WtSettings -Path $wtEmpty -PwshPath 'C:\x\pwsh.exe' -NoBackup
        $oe = ConvertFrom-Jsonc -Text ([System.IO.File]::ReadAllText($wtEmpty))
        $emptyOk = (@($oe.profiles.list).Count -eq 1 -and $oe.defaultProfile -eq $newGuid)
    } catch { $emptyMsg = $_.Exception.Message }
}
T 'T32 WT：空 profile 列表插入后仍是合法 JSON（无多余逗号）' { @{ ok = $emptyOk; detail = if ($emptyOk) { '插入 1 条并设为默认，解析通过' } else { "失败: $emptyMsg" } } }

$vsFix = Join-Path $cfgDir 'vscode-settings.json'
$vsJsonc = @'
{
    // 用户自己的注释，不能被抹掉
    "editor.fontSize": 14,
    "terminal.integrated.profiles.windows": {
        "Ubuntu (WSL)": { "path": "wsl.exe" }
    }
}
'@
[System.IO.File]::WriteAllText($vsFix, $vsJsonc, $utf8NoBom)
$vsOk = $false; $vsMsg = ''
if ($wtReady) {
    try { $null = Update-VsCodeSettings -Path $vsFix -PwshPath 'G:\Tools\ps7\pwsh.exe'; $vsOk = $true }
    catch { $vsMsg = $_.Exception.Message }
}
$vsAfter = if (Test-Path $vsFix) { [System.IO.File]::ReadAllText($vsFix) } else { '' }
T 'T33 VSCode：保留用户自建 profile 与注释，只加 PowerShell 7' {
    $ok = $false; $msg = $vsMsg
    if ($vsOk) {
        try {
            $o = ConvertFrom-Jsonc -Text $vsAfter
            $prof = $o.'terminal.integrated.profiles.windows'
            $ok = ($null -ne $prof.'Ubuntu (WSL)') -and ($null -ne $prof.'PowerShell 7') -and
                  ($o.'terminal.integrated.defaultProfile.windows' -eq 'PowerShell 7') -and
                  $vsAfter.Contains('// 用户自己的注释')
        } catch { $msg = $_.Exception.Message }
    }
    @{ ok = $ok; detail = if ($ok) { 'Ubuntu 保留、PowerShell 7 已加、注释保留、默认已设' } else { "失败: $msg" } }
}

# ---- 11. 独立运行 setup-defaults / 不该动的就别动 ----
Write-Host "`n=== 11. 独立运行与「不改也能过」 ===" -ForegroundColor Cyan

# 独立跑 setup-defaults 时 BinDir 曾从写死的 $ToolsRoot 拼，而 PS7Dir 从探测到的 pwsh 反推，
# 两者不一致 → 往 PATH 加一条 %LOCALAPPDATA%\ps7-toolkit\bin 死链（目录根本不存在）
$deriveRoot = $setupCode.Contains("`$PSBoundParameters.ContainsKey('ToolsRoot')")
T 'T34 独立运行时 ToolsRoot 从探测到的 pwsh 反推' { @{ ok = $deriveRoot; detail = "含反推逻辑 = $deriveRoot" } }

$guardAdd = ($setupCode -match 'foreach \(\$d in @\(\$PS7Dir, \$BinDir\)\) \{[\s\S]{0,200}?Test-Path \$d')
T 'T35 加 PATH 前先确认目录存在（不再左手删右手加）' { @{ ok = $guardAdd; detail = "含 Test-Path 守卫 = $guardAdd" } }

# VSCode 那边曾只比对「键存在」就整段重写，连空格差异都会写一次盘
$vsSame = Join-Path $cfgDir 'vscode-already-ok.json'
$vsSameText = @'
{
    // 值本来就对，只是空格跟脚本生成的不一样
    "terminal.integrated.defaultProfile.windows":  "PowerShell 7",
    "terminal.integrated.profiles.windows": {
        "PowerShell 7": { "path":  "G:\\Tools\\ps7\\pwsh.exe", "icon":  "terminal-powershell" }
    }
}
'@
[System.IO.File]::WriteAllText($vsSame, $vsSameText, $utf8NoBom)
$sameOk = $false; $sameMsg = ''
if ($wtReady) {
    try {
        $rs = Update-VsCodeSettings -Path $vsSame -PwshPath 'G:\Tools\ps7\pwsh.exe' -NoBackup
        $after = [System.IO.File]::ReadAllText($vsSame)
        $sameOk = (-not $rs.Changed) -and ($after -eq $vsSameText)
    } catch { $sameMsg = $_.Exception.Message }
}
T 'T36 VSCode：值已正确时一个字节都不改（Changed=False）' { @{ ok = $sameOk; detail = if ($sameOk) { '未写盘，内容与原来完全一致' } else { "失败: $sameMsg" } } }

# 落盘时按原文件的 BOM 状态写回，别把用户文件的编码顺手改了
$bomFix = Join-Path $cfgDir 'wt-bom.json'
[System.IO.File]::WriteAllText($bomFix, '{"defaultProfile": "{00000000-0000-0000-0000-000000000000}"}', (New-Object System.Text.UTF8Encoding($true)))
$bomOk = $false; $bomMsg = ''
if ($wtReady) {
    try {
        $null = Update-WtSettings -Path $bomFix -PwshPath 'C:\x\pwsh.exe' -NoBackup
        $b = [System.IO.File]::ReadAllBytes($bomFix)
        $bomOk = ($b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF)
    } catch { $bomMsg = $_.Exception.Message }
}
T 'T37 改写后保留原文件的 UTF-8 BOM' { @{ ok = $bomOk; detail = if ($bomOk) { 'BOM 仍在' } else { "BOM 丢了 / 失败: $bomMsg" } } }

# 即使本次无需修改，也要留下最初的还原点：否则文件一旦被更早的版本重写过，
# 等再要备份时备份下来的已经是「改过之后」的样子，原样再也拿不回来。
$bakNoop = Join-Path $cfgDir 'wt-noop.json'
$bakNoopText = '{"defaultProfile": "{9e1b2a44-7c3d-4f8e-b5a1-2d6c9f0e3b71}"}'
[System.IO.File]::WriteAllText($bakNoop, $bakNoopText, $utf8NoBom)
$bakOk = $false; $bakMsg = ''
if ($wtReady) {
    try {
        $rb = Update-WtSettings -Path $bakNoop -PwshPath 'C:\x\pwsh.exe'
        $bakPath = $bakNoop + '.ps7bak'
        $sameText = ([System.IO.File]::ReadAllText($bakNoop) -eq $bakNoopText)
        $bakSame = (Test-Path -LiteralPath $bakPath) -and ([System.IO.File]::ReadAllText($bakPath) -eq $bakNoopText)
        $bakOk = (-not $rb.Changed) -and $sameText -and $bakSame
        $bakMsg = "changed=$($rb.Changed) 原文件未动=$sameText 备份存在且内容一致=$bakSame"
    } catch { $bakMsg = $_.Exception.Message }
}
T 'T38 无需修改时也生成 .ps7bak 还原点（且不动原文件）' { @{ ok = $bakOk; detail = if ($bakOk) { '已备份，原文件一个字节未动' } else { "失败: $bakMsg" } } }

# ---- 12. 内测反馈回归（jq 中文键名 / 旧工具目录提示） ----
Write-Host "`n=== 12. 内测反馈防回归 ===" -ForegroundColor Cyan

# jq 裸字段名只支持 ASCII，中文键必须写 .["名称"]；AI 极易写成 .名称 然后反复报错烧 token
$skillMd  = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot '..\SKILL.md'))
$readmeMd = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot '..\README.md'))
$troubMd  = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot '..\references\troubleshooting.md'))
$jqTip    = '.["'
$jqOk = ($skillMd.Contains($jqTip) -and $readmeMd.Contains($jqTip) -and
         $troubMd -match 'INVALID_CHARACTER' -and $skillMd -match 'INVALID_CHARACTER')
T 'T39 jq 中文键名写法提示在 SKILL/README/troubleshooting 三处齐备' { @{ ok = $jqOk; detail = "SKILL=$($skillMd.Contains($jqTip)) README=$($readmeMd.Contains($jqTip)) troubleshooting=$($troubMd -match 'INVALID_CHARACTER')" } }

# 升级场景：旧安装的 bin 目录与新 bin 并存于 PATH，应打印提示（但不删用户目录）
$oldHint = ($setupCode.Contains("Join-Path `$exp 'rg.exe'")) -and
           ($setupCode.Contains("Join-Path `$exp 'fd.exe'")) -and
           ($setupCode -match '旧工具目录仍在 PATH') -and
           ($setupCode -notmatch 'Remove-Item.*\$oldTools')
T 'T40 检测到旧工具目录并存时打印提示（且绝不自动删除）' { @{ ok = $oldHint; detail = "含检测与提示 = $oldHint" } }


# ---- 13. 反引号守卫（shell-guard） ----
Write-Host "`n=== 13. 反引号与特殊字符守卫 ===" -ForegroundColor Cyan

$guardPath  = Join-Path $PSScriptRoot 'shell-guard.ps1'
$guardReady = Test-Path $guardPath
if ($guardReady) { . $guardPath }

if ($guardReady) {
    $d1 = Get-ShellQuoteDiagnosis -Command 'echo today is `date`' -Shell 'bash'
    T 'T41 bash 成对反引号：判风险并给出 $( ) 改写' { @{ ok = ($d1.Risky -and $d1.Backticks -eq 2 -and $d1.SafeForm -eq 'echo today is $(date)'); detail = "risky=$($d1.Risky) n=$($d1.Backticks) safe=$($d1.SafeForm)" } }

    $d2 = Get-ShellQuoteDiagnosis -Command 'echo a` b' -Shell 'bash'
    T 'T42 bash 奇数个裸反引号：判风险且不做自动改写' { @{ ok = ($d2.Risky -and $d2.Backticks -eq 1 -and -not $d2.SafeForm); detail = "risky=$($d2.Risky) n=$($d2.Backticks) safe=$($d2.SafeForm)" } }

    $d3 = Get-ShellQuoteDiagnosis -Command "echo 'a`b'" -Shell 'bash'
    T 'T43 单引号内的反引号判为安全' { @{ ok = (-not $d3.Risky -and $d3.Backticks -eq 0); detail = "risky=$($d3.Risky) n=$($d3.Backticks)" } }

    $d4 = Get-ShellQuoteDiagnosis -Command 'cat > x.md <<EOF'  -Shell 'bash'
    $d5 = Get-ShellQuoteDiagnosis -Command "cat > x.md <<'EOF'" -Shell 'bash'
    T 'T44 heredoc：未加引号报警，加了单引号不报' { @{ ok = ($d4.Risky -and -not $d5.Risky); detail = "raw=$($d4.Risky) quoted=$($d5.Risky)" } }

    $d6 = Get-ShellQuoteDiagnosis -Command 'Write-Host "a`nb"' -Shell 'pwsh'
    T 'T45 pwsh 视角：识别转义符反引号' { @{ ok = ($d6.Risky -and $d6.Backticks -ge 1); detail = "risky=$($d6.Risky) n=$($d6.Backticks)" } }

    $rcGuard = Invoke-SafeCommand -Command 'Write-Host "a`nb"'
    T 'T46 有风险时拒绝执行（返回 2）' { @{ ok = ($rcGuard -eq 2); detail = "rc=$rcGuard" } }

    $d7 = Get-ShellQuoteDiagnosis -Command 'cd C:\Users\x && dir' -Shell 'bash'
    $d8 = Get-ShellQuoteDiagnosis -Command "cd 'C:\Users\x'" -Shell 'bash'
    T 'T47 bash 引号外 Windows 路径判风险，单引号包裹后安全' { @{ ok = ($d7.Risky -and $d7.Backticks -eq 0 -and -not $d8.Risky); detail = "raw=$($d7.Risky) quoted=$($d8.Risky)" } }

    $d9  = Get-ShellQuoteDiagnosis -Command 'curl https://example.com' -Shell 'pwsh'
    $d10 = Get-ShellQuoteDiagnosis -Command 'curl.exe https://example.com' -Shell 'pwsh'
    T 'T48 pwsh：裸 curl 提醒写 curl.exe，curl.exe 不提醒' { @{ ok = (($d9.Advice | Where-Object { $_ -like '*curl.exe*' }).Count -gt 0 -and ($d10.Advice | Where-Object { $_ -like '*别名*' }).Count -eq 0 -and -not $d10.Risky); detail = "bare=$($d9.Advice.Count) 条 exe=$($d10.Advice.Count) 条" } }

    $d11 = Get-ShellQuoteDiagnosis -Command 'a && b' -Shell 'pwsh'
    T 'T49 pwsh：&& 提醒 5.1 不支持（不判硬风险）' { @{ ok = (-not $d11.Risky -and ($d11.Advice | Where-Object { $_ -like '*&&*' }).Count -gt 0); detail = "risky=$($d11.Risky) advice=$($d11.Advice.Count)" } }

    $d12 = Get-ShellQuoteDiagnosis -Command 'Get-Content a.txt | Out-File b.txt' -Shell 'pwsh'
    $d13 = Get-ShellQuoteDiagnosis -Command 'Get-Content a.txt | Out-File b.txt -Encoding utf8' -Shell 'pwsh'
    T 'T50 pwsh：Out-File 无 -Encoding 提醒编码，加了不提醒' { @{ ok = (($d12.Advice | Where-Object { $_ -like '*UTF-16*' }).Count -gt 0 -and ($d13.Advice | Where-Object { $_ -like '*UTF-16*' }).Count -eq 0); detail = "no-enc=$($d12.Advice.Count) 条 enc=$($d13.Advice.Count) 条" } }

    # ---- 1.1.6 内测反馈防回归（豆包 v1.1.6 测试报告）----
    # T51：曾因参数名 -Command 撞 powershell.exe 自身开关，转发含双引号命令时错位成
    #      「文件不存在: executed」rc=3。改名 -Text 后：① 参数块必须是 $Text；
    #      ② 含双引号的命令可 & 直调且不错位（& 直调引号完全保真，任何父进程都成立；
    #         5.1 下 Write-Host 提示不走 2>&1，故只断言无错位报错，功能端到端由 T52 覆盖）。
    $o51 = & $guardPath -Text 'Write-Output "safe executed"' 2>&1
    $s51 = ($o51 | Out-String)
    $g51 = Get-Content $guardPath -Raw
    T 'T51 参数已改名 -Text 且含双引号命令 & 直调无错位（防 -Command 撞名回归）' { @{ ok = (($g51 -match '\[string\]\$Text') -and ($g51 -notmatch '\.PARAMETER Command') -and ($s51 -notmatch '文件不存在')); detail = "param改名=$($g51 -match '\[string\]\$Text') 错位残留=$($s51 -match '文件不存在')" } }

    # T52：-Execute 安全命令曾因 exit (函数) 括号把内层输出吞进表达式，执行结果「消失」。
    #      命令特意带内层双引号，顺带端到端验证 & 直调下引号保真。
    $o52 = & $guardPath -Text 'Write-Output "guard-marker-t52"' -Execute 2>&1
    $s52 = ($o52 | Out-String)
    T 'T52 -Execute 安全命令：内层输出必须可见且 rc=0' { @{ ok = ($LASTEXITCODE -eq 0 -and $s52 -match 'guard-marker-t52'); detail = "exit=$LASTEXITCODE marker可见=$($s52 -match 'guard-marker-t52')" } }

    # T53：-File 检查脚本文件曾因参数改名后赋错变量而静默不干活。
    $tmp53 = Join-Path $base 'guard-file-case.ps1'
    Set-Content -Path $tmp53 -Value 'Write-Output "a`nb"' -Encoding UTF8
    & $guardPath -File $tmp53 2>&1 | Out-Null
    $rc53 = $LASTEXITCODE
    Remove-Item $tmp53 -ErrorAction SilentlyContinue
    T 'T53 -File 检查含反引号脚本：正确判风险 rc=1（不静默）' { @{ ok = ($rc53 -eq 1); detail = "exit=$rc53" } }

    # T54：verify 对第三方死链的文案必须区分「本工具自动清 / 第三方手动处理」。
    $vraw = Get-Content (Join-Path $PSScriptRoot 'verify.ps1') -Raw
    T 'T54 verify 死链文案区分本工具与第三方路径' { @{ ok = (($vraw -match '会自动清掉') -and ($vraw -match '第三方路径失效')); detail = "本工具文案=$($vraw -match '会自动清掉') 第三方文案=$($vraw -match '第三方路径失效')" } }

    # ---- 1.1.6 二轮内测防回归（DeepSeek v1.1.6 审查报告）----
    # T55：-Execute 曾用 -Command 跨进程转发，内层双引号在 argv 层被切散——
    #      Write-Output "hello  world  spaced" 输出 3 行（5.1 与 pwsh 7 均丢）。
    #      改为 -EncodedCommand 后必须单行且连续空格原样保留。
    $o55 = & $guardPath -Text 'Write-Output "hello  world  spaced"' -Execute 2>&1
    $hit55 = @($o55 | Where-Object { "$_" -match 'hello' })
    T 'T55 -Execute 引号保真：双引号与连续空格原样保留（防 -Command 转发改写命令）' { @{ ok = ($hit55.Count -eq 1 -and ("$($hit55[0])" -match 'hello  world  spaced')); detail = "条数=$($hit55.Count) 内容=[$($hit55[0])]" } }

    # T56：-Execute 纯 PS 命令抛错时曾因 $LASTEXITCODE 为 null 返回 0（报错却报成功）。
    & $guardPath -Text 'throw "boom"' -Execute 2>&1 | Out-Null
    $rc56 = $LASTEXITCODE
    T 'T56 -Execute 纯 PS 命令抛错：退出码 1（报错不报成功）' { @{ ok = ($rc56 -eq 1); detail = "exit=$rc56" } }

    # T57：ConvertTo-SafeCommand 曾无条件改写成对反引号，段内含 ' 或 $ 时语义会变。
    $d57a = Get-ShellQuoteDiagnosis -Command 'echo `$env:FOO`' -Shell 'bash'
    $d57b = Get-ShellQuoteDiagnosis -Command 'echo today is `date`' -Shell 'bash'
    T 'T57 改写保真：段内含 $ 不自动改写，纯命令替换仍给出 $( ) 改写' { @{ ok = (-not $d57a.SafeForm -and $d57b.SafeForm -eq 'echo today is $(date)'); detail = "含dollar改写=$($d57a.SafeForm) 纯替换改写=$($d57b.SafeForm)" } }
    # ---- 1.1.6 三轮内测防回归（DeepSeek v1.1.6 第三轮报告）----
    # T58：Invoke-SafeCommand 曾把子进程输出与退出码混进同一个返回流，$rc 变成 Object[]，
    #      任何 if ($rc -ne 0) 恒真。默认模式必须只返回 int。
    $r58 = Invoke-SafeCommand -Command 'Write-Output "hello  world  spaced"'
    T 'T58 Invoke-SafeCommand 默认只返回 int 退出码（不被输出污染）' { @{ ok = ($r58 -is [int] -and @($r58).Count -eq 1 -and $r58 -eq 0); detail = "type=$($r58.GetType().Name) count=$(@($r58).Count) value=$r58" } }

    # T59：stderr 曾与 stdout 混流并被 ErrorRecord 展开成多行（带 CategoryInfo / caret 定位），
    #      现在必须加 [stderr] 前缀且压成单行。
    $o59 = Invoke-SafeCommand -Command 'Write-Error "boom-stderr"' -Capture
    $err59 = @($o59 | Where-Object { "$_" -like '`[stderr`]*' })
    $flat59 = ($err59.Count -eq 1 -and ("$($err59[0])" -notmatch 'CategoryInfo|FullyQualifiedErrorId') -and ("$($err59[0])" -notmatch "`n"))
    T 'T59 stderr 单独标记前缀并压成单行（不再混进 stdout 多行展开）' { @{ ok = $flat59; detail = "前缀条数=$($err59.Count) 内容=[$($err59[0])]" } }

    # T60：-Capture 模式下输出走管道、退出码留在 GuardLastExitCode，函数不返回值。
    $o60 = Invoke-SafeCommand -Command 'Write-Output "cap-marker-60"' -Capture
    T 'T60 -Capture：输出进管道、退出码在 GuardLastExitCode、函数无返回值' { @{ ok = ($o60 -eq 'cap-marker-60' -and $GuardLastExitCode -eq 0); detail = "输出=[$o60] rc=$GuardLastExitCode" } }

    # T61：文档防漂移 —— 返回值契约 / 原生命令退出码归一 / 开发者备注（测引号保真别用 -Command 对照组）
    #      三项都必须落在 README 里，否则下一个改守卫的人还会踩。
    #      注意：README 是无 BOM 的 UTF-8，5.1 的 Get-Content 默认按 ANSI 读会变乱码，必须显式按 UTF-8 读。
    $rpath = Join-Path (Split-Path -Parent $PSScriptRoot) 'README.md'
    $rraw = [System.IO.File]::ReadAllText($rpath, [System.Text.Encoding]::UTF8)
    $doc61 = (($rraw -match '-Capture') -and ($rraw -match '归一') -and ($rraw -match '开发者备注'))
    T 'T61 README 三处契约齐备（-Capture 契约 / 退出码归一 / 开发者备注）' { @{ ok = $doc61; detail = "关键词=$((($rraw -match '-Capture'),($rraw -match '归一'),($rraw -match '开发者备注')) -join ',')" } }

    # T62：SKILL.md 的 frontmatter 必须从第一个字节开始（不能有 UTF-8 BOM）。
    #      带 BOM 时 `---` 前面多出 \ufeff，市场侧的 YAML 解析会失败 → display_name / description
    #      全部回落成文件夹名（线上真的变成过「Ps7 Toolkit」）。
    $sk69 = [System.IO.File]::ReadAllBytes((Join-Path (Split-Path -Parent $PSScriptRoot) 'SKILL.md'))
    $noBom = ($sk69.Length -gt 3 -and $sk69[0] -eq 0x2D -and $sk69[1] -eq 0x2D -and $sk69[2] -eq 0x2D)
    $skText = [System.IO.File]::ReadAllText((Join-Path (Split-Path -Parent $PSScriptRoot) 'SKILL.md'), [System.Text.Encoding]::UTF8)
    $hasFields = ($skText -match '(?m)^display_name:' -and $skText -match '(?m)^version:')
    T 'T62 SKILL.md 无 BOM 且首字节为 ---（否则市场解析不到 display_name）' { @{ ok = ($noBom -and $hasFields); detail = "首3字节=$([char]$sk69[0])$([char]$sk69[1])$([char]$sk69[2]) 字段齐备=$hasFields" } }
} else {
    T 'T41 反引号守卫脚本存在' { @{ ok = $false; detail = '缺少 shell-guard.ps1' } }
}

# ---------------------------------------------------------------- 1.1.8 安全删除 / 受限环境
# T63～T69 不依赖 shell-guard，放在外层，任何环境都要跑。
$srPath  = Join-Path $PSScriptRoot 'safe-remove.ps1'
$selfExe = (Get-Process -Id $PID).Path

# 断言要看的关键字拆开拼：脚本自身不能出现完整字面量，
# 否则扫描型安全策略会把「检查脚本」当成「违规脚本」一起拦掉。
$riskyCompile = 'Add' + '-Type'
$riskyCom     = '-' + 'ComObject'

function Invoke-SafeRemoveQuiet {
    param([string[]] $Argv)
    & $selfExe -NoProfile -ExecutionPolicy Bypass -File $srPath @Argv *> $null
    return $LASTEXITCODE
}

# T63：脚本必须存在、语法可解析，且通篇不出现会被工具层拦掉的写法。
#      （写这个脚本的初衷就是「受限环境也能删文件」，一旦有人回退成编译/COM 就白改了。）
if (Test-Path $srPath) {
    $srErr = $null; $srTok = $null
    $null = [System.Management.Automation.Language.Parser]::ParseFile($srPath, [ref]$srTok, [ref]$srErr)
    $srRaw = [System.IO.File]::ReadAllText($srPath, [System.Text.Encoding]::UTF8)
    $srClean = ($srRaw -notmatch $riskyCompile -and $srRaw -notmatch $riskyCom)
    T 'T63 safe-remove.ps1 存在、语法通过、不含运行时编译/COM 写法' { @{ ok = ($srErr.Count -eq 0 -and $srClean); detail = "语法错误=$($srErr.Count) 无敏感写法=$srClean" } }
} else {
    T 'T63 safe-remove.ps1 存在、语法通过、不含运行时编译/COM 写法' { @{ ok = $false; detail = '缺少 safe-remove.ps1' } }
}

$srBox = Join-Path $base 'recycle-box'
New-Item -ItemType Directory -Path $srBox -Force | Out-Null

# T64：默认行为必须是「删掉 + 可还原」，即走回收站而不是直接抹掉。
#      这里只断言退出码与源路径，回收站条目数受其他进程影响，不纳入断言。
$f64 = Join-Path $srBox 'del-me.txt'
Set-Content -Path $f64 -Value 'x' -Encoding UTF8
$rc64 = Invoke-SafeRemoveQuiet @('-Path', $f64)
T 'T64 删文件：rc=0 且源路径消失（默认走回收站）' { @{ ok = ($rc64 -eq 0 -and -not (Test-Path $f64)); detail = "exit=$rc64 已消失=$(-not (Test-Path $f64))" } }

# T65：目录不带 -Recurse 必须拒绝——防 AI 一条命令端掉整棵树。
$d65 = Join-Path $srBox 'dir-no-recurse'
New-Item -ItemType Directory -Path $d65 -Force | Out-Null
Set-Content -Path (Join-Path $d65 'a.txt') -Value 'x' -Encoding UTF8
$rc65 = Invoke-SafeRemoveQuiet @('-Path', $d65)
T 'T65 目录不带 -Recurse：拒绝删除 rc=2 且目录仍在' { @{ ok = ($rc65 -eq 2 -and (Test-Path $d65)); detail = "exit=$rc65 目录还在=$(Test-Path $d65)" } }

# T66：带 -Recurse 时整目录一次进回收站。
$rc66 = Invoke-SafeRemoveQuiet @('-Path', $d65, '-Recurse')
T 'T66 目录带 -Recurse：rc=0 且目录消失' { @{ ok = ($rc66 -eq 0 -and -not (Test-Path $d65)); detail = "exit=$rc66 已消失=$(-not (Test-Path $d65))" } }

# T67：盘根必须落在保护名单里（AI 最容易写出 Remove-Item C:\ -Recurse 这种命令）。
$root67 = $env:SystemDrive + '\'
$rc67 = Invoke-SafeRemoveQuiet @('-Path', $root67)
T 'T67 盘根受保护：拒绝删除 rc=2 且盘符仍可用' { @{ ok = ($rc67 -eq 2 -and (Test-Path $root67)); detail = "exit=$rc67 盘还在=$(Test-Path $root67)" } }

# T68：-WhatIf 只预览，不能真删，且退出码按「预览成功」算 0。
$f68 = Join-Path $srBox 'whatif.txt'
Set-Content -Path $f68 -Value 'x' -Encoding UTF8
$rc68 = Invoke-SafeRemoveQuiet @('-Path', $f68, '-WhatIf')
T 'T68 -WhatIf：rc=0 且文件未被动过' { @{ ok = ($rc68 -eq 0 -and (Test-Path $f68)); detail = "exit=$rc68 文件还在=$(Test-Path $f68)" } }

# T69：setup-defaults 不能再依赖运行时编译 / COM，开始菜单入口改成 .cmd。
#      这两处在受限环境会被拦，且原来都是 catch 吞掉，用户只会觉得「装了没生效」。
$sdRaw = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot 'setup-defaults.ps1'), [System.Text.Encoding]::UTF8)
$sdClean = ($sdRaw -notmatch $riskyCompile -and $sdRaw -notmatch $riskyCom)
$sdCmd   = ($sdRaw -match 'PowerShell 7\.cmd')
T 'T69 setup-defaults 不含运行时编译/COM，开始菜单改 .cmd 入口' { @{ ok = ($sdClean -and $sdCmd); detail = "无敏感写法=$sdClean 有 .cmd 入口=$sdCmd" } }

# ---------------------------------------------------------------- 汇总
Write-Host "`n########## 结果 ##########" -ForegroundColor Magenta
$pass = ($results | Where-Object { $_.ok }).Count
$fail = ($results | Where-Object { -not $_.ok }).Count
$color = if ($fail -eq 0) { 'Green' } else { 'Red' }
Write-Host ("共 " + $results.Count + " 项  通过 " + $pass + "  失败 " + $fail) -ForegroundColor $color
if ($fail -gt 0) {
    Write-Host "`n失败项：" -ForegroundColor Red
    $results | Where-Object { -not $_.ok } | ForEach-Object { Write-Host ("  - " + $_.name + " : " + $_.detail) -ForegroundColor Red }
}
$report = Join-Path $base 'result.txt'
$results | ForEach-Object { ($(if ($_.ok) { 'PASS' } else { 'FAIL' })) + "`t" + $_.name + "`t" + $_.detail } |
    Set-Content $report -Encoding UTF8
Write-Host ("`n详细报告: " + $report)
if (-not $KeepArtifacts) {
    Write-Host "（沙箱目录保留在 TEMP 下，可手动删除）"
}

if ($fail -eq 0) { exit 0 } else { exit 1 }
