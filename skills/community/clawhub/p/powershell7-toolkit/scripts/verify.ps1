#Requires -Version 5.1
<#
.SYNOPSIS
    体检脚本：检查 PowerShell 7 / Rust 工具 / 默认化配置是否到位，并输出诊断报告。
.PARAMETER ToolsRoot
    安装根目录，默认 $env:LOCALAPPDATA\ps7-toolkit
.PARAMETER PwshPath
    指定 pwsh.exe 路径。不填则自动探测。
.PARAMETER BinDir
    指定 Rust 工具目录。不填则自动探测。
.PARAMETER Json
    额外输出 JSON（便于其它程序解析）
.PARAMETER SkipDefaults
    安装时用了 -SkipDefaults（只装不配）：此时不检查 profile / 注册表 / 快捷方式 / PATH，
    这些项目会标成「已跳过」而不是「失败」。
#>
[CmdletBinding()]
param(
    [string]$ToolsRoot = (Join-Path $env:LOCALAPPDATA 'ps7-toolkit'),
    [string]$PwshPath,
    [string]$BinDir,
    [switch]$Json,
    [switch]$SkipDefaults
)

$ErrorActionPreference = 'SilentlyContinue'
$report = [ordered]@{}

Write-Host "`n########## PowerShell 7 工具链体检 ##########" -ForegroundColor Magenta

# 0. 探测 pwsh
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
        if (Test-Path $k) { $v = (Get-ItemProperty $k).'(default)'; if ($v) { $cands += $v } }
    }
    foreach ($c in ($cands | Where-Object { $_ } | Select-Object -Unique)) { if (Test-Path $c) { $PwshPath = $c; break } }
}
if (-not $BinDir) {
    $BinDir = Join-Path $ToolsRoot 'bin'
}

# 1. PowerShell 7
Write-Host "`n[1] PowerShell 7"
$ver = $null
if ($PwshPath -and (Test-Path $PwshPath)) {
    try { $ver = (& $PwshPath -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' | Select-Object -First 1) } catch { }
}
if ($ver) { Write-Host ("    [OK] {0}  ->  {1}" -f $ver, $PwshPath) -ForegroundColor Green }
else { Write-Host "    [X] 未安装或不可用" -ForegroundColor Red }
$report['pwsh'] = @{ path = $PwshPath; version = $ver; ok = [bool]$ver }

# 2. Rust 工具
Write-Host "`n[2] Rust 高性能工具"
$tools = @{}
foreach ($t in 'rg','fd','fzf','bat','delta','jq') {
    $exe = Join-Path $BinDir "$t.exe"
    $src = $exe
    if (-not (Test-Path $exe)) {
        $g = Get-Command $t -ErrorAction SilentlyContinue
        if ($g) { $src = $g.Source }
    }
    if ($src -and (Test-Path $src)) {
        $v = (& $src --version 2>$null | Select-Object -First 1)
        Write-Host ("    [OK] {0,-6} {1}" -f $t, $v) -ForegroundColor Green
        $tools[$t] = $v
    } else {
        Write-Host ("    [X] {0,-6} 未安装" -f $t) -ForegroundColor Red
        $tools[$t] = $null
    }
}
$report['tools'] = $tools
$report['binDir'] = $BinDir

# 3. profile
Write-Host "`n[3] PowerShell profile（UTF-8 根治）"
if ($SkipDefaults) {
    Write-Host "    [-] 已跳过（-SkipDefaults 只装不配）" -ForegroundColor DarkGray
} else {
    $docs = [Environment]::GetFolderPath('MyDocuments')
    foreach ($p in @((Join-Path $docs 'WindowsPowerShell\Microsoft.PowerShell_profile.ps1'), (Join-Path $docs 'PowerShell\Microsoft.PowerShell_profile.ps1'))) {
        if ((Test-Path $p) -and ((Get-Content $p -Raw) -match 'ps7-toolkit')) { Write-Host "    [OK] $p" -ForegroundColor Green }
        else { Write-Host "    [X] $p" -ForegroundColor Red }
    }
}

# 4. 注册表与关联
Write-Host "`n[4] 注册表与文件关联"
if ($SkipDefaults) {
    Write-Host "    [-] 已跳过（-SkipDefaults 只装不配）" -ForegroundColor DarkGray
} else {
    foreach ($c in @(
        @{ n = 'App Paths\pwsh.exe'; p = 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe' },
        @{ n = '.ps1 关联';         p = 'HKCU:\Software\Microsoft\Classes\.ps1\shell\open\command' })) {
        if (Test-Path $c.p) { Write-Host ("    [OK] " + $c.n) -ForegroundColor Green }
        else { Write-Host ("    [X] " + $c.n) -ForegroundColor Red }
    }
    # 默认终端程序：真正生效的位置是 HKCU\Console\%%Startup 的两个 GUID 值，
    # 不是 Explorer\Advanced（那个键是系统自带的，永远存在，查它等于没查）。
    $startup = 'HKCU:\Console\%%Startup'
    $wtConsole = '{2EACA947-7F5F-4CFA-BA87-8F7FBEEFBE69}'
    $consoleHost = '{B23D10C0-E52E-411E-9D5B-C09FDF709C7D}'
    $autoPick = '{00000000-0000-0000-0000-000000000000}'
    $dc = $null
    if (Test-Path $startup) { $dc = (Get-ItemProperty -Path $startup -Name 'DelegationConsole' -ErrorAction SilentlyContinue).DelegationConsole }
    if (-not $dc -or $dc -eq $autoPick) {
        # 全 0 GUID 不是「没设」，是「交给 Windows 自动选」——别当成已配置
        Write-Host "    [!] 默认终端程序 = 自动选择（未显式指定；Win11 22H2+ 通常会自动用 Windows Terminal）" -ForegroundColor Yellow
    } elseif ($dc -eq $wtConsole) {
        Write-Host "    [OK] 默认终端程序 = Windows Terminal" -ForegroundColor Green
    } elseif ($dc -eq $consoleHost) {
        Write-Host "    [!] 默认终端程序 = 旧的控制台宿主（想换回 Windows Terminal 请重跑 setup-defaults.ps1）" -ForegroundColor Yellow
    } else {
        Write-Host "    [OK] 默认终端程序已指定: $dc" -ForegroundColor Green
    }
}

# 5. 应用层
Write-Host "`n[5] 应用层配置"
if ($SkipDefaults) {
    Write-Host "    [-] 已跳过（-SkipDefaults 只装不配）" -ForegroundColor DarkGray
} else {
    $lnk = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\PowerShell 7.lnk'
    if (Test-Path $lnk) { Write-Host "    [OK] 开始菜单 PowerShell 7" -ForegroundColor Green } else { Write-Host "    [X] 开始菜单 PowerShell 7" -ForegroundColor Red }
    $wt = Join-Path $env:LOCALAPPDATA 'Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json'
    if (Test-Path $wt) {
        $c = Get-Content $wt -Raw -Encoding UTF8 | ConvertFrom-Json
        $hit = $c.profiles.list | Where-Object { $_.name -eq 'PowerShell 7' }
        if ($hit -and $c.defaultProfile -eq $hit.guid) { Write-Host "    [OK] Windows Terminal 默认 = PS7" -ForegroundColor Green }
        else { Write-Host "    [!] Windows Terminal 未指向 PS7" -ForegroundColor Yellow }
    } else { Write-Host "    [-] 未安装 Windows Terminal" -ForegroundColor DarkGray }
}

# 6. PATH
Write-Host "`n[6] PATH"
if ($SkipDefaults) {
    Write-Host "    [-] 已跳过（-SkipDefaults 不改 PATH）" -ForegroundColor DarkGray
} else {
    $up = [Environment]::GetEnvironmentVariable('Path','User')
    # 逐项比较：以前用 IndexOf / -like 做子串包含，会把「路径里恰好含这几个字」误判成已配置，
    # 也从不检查目录是否还存在，于是 PATH 里留着死链也照样打 OK。
    $entries = @()
    if ($up) {
        foreach ($e in $up.Split(';')) {
            $t = $e.Trim()
            if ($t) { $entries += $t.TrimEnd('\') }
        }
    }
    $ps7dir = if ($PwshPath) { (Split-Path -Parent $PwshPath).TrimEnd('\') } else { $null }
    foreach ($d in @($ps7dir, $BinDir)) {
        if (-not $d) { continue }
        $d = $d.TrimEnd('\')
        $hit = $false
        foreach ($e in $entries) { if ([string]::Equals($e, $d, [StringComparison]::OrdinalIgnoreCase)) { $hit = $true; break } }
        if (-not $hit) {
            # 目录能用但没进 PATH：不算失败，只是新开的终端里敲不到短命令
            Write-Host "    [!] $d 不在用户 PATH（工具本身可用，需用绝对路径或手动加 PATH）" -ForegroundColor Yellow
        } elseif (-not (Test-Path $d)) {
            Write-Host "    [X] $d 在 PATH 里但目录不存在（死链）" -ForegroundColor Red
        } else {
            Write-Host "    [OK] $d" -ForegroundColor Green
        }
    }
    # 顺带把 PATH 里过期/失效的项点出来（只提示，不自动改）
    $dead = @()
    foreach ($e in $entries) {
        $exp = [Environment]::ExpandEnvironmentVariables($e)
        if (-not (Test-Path $exp)) { $dead += $e }
    }
    if ($dead.Count -gt 0) {
        Write-Host ("    [!] 用户 PATH 里有 {0} 项指向不存在的目录（死链，不影响使用）：" -f $dead.Count) -ForegroundColor Yellow
        $own = @($dead | Where-Object { $_ -like '*ps7-toolkit*' })
        $other = @($dead | Where-Object { $_ -notlike '*ps7-toolkit*' })
        if ($own.Count -gt 0) {
            Write-Host "        属于本工具的失效路径（重跑 setup-defaults.ps1 会自动清掉）：" -ForegroundColor DarkGray
            foreach ($e in $own) { Write-Host "          - $e" -ForegroundColor DarkGray }
        }
        if ($other.Count -gt 0) {
            Write-Host "        第三方路径失效（本工具不会动它，需你自行决定是否手动清理）：" -ForegroundColor DarkGray
            foreach ($e in $other) { Write-Host "          - $e" -ForegroundColor DarkGray }
        }
    }
}

if ($Json) { Write-Host "`n----JSON----"; Write-Host ($report | ConvertTo-Json -Depth 6) }
Write-Host "`n体检结束。`n"
