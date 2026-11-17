#Requires -Version 5.1
<#
.SYNOPSIS
    PowerShell 7 + Rust 高性能工具链 —— 一键安装器（跨机器可移植 / 幂等 / 免管理员）
.DESCRIPTION
    策略：先"探测"系统已装的 pwsh（多路径 + 注册表 + PATH + scoop/choco/Store），
          探测到就直接复用；探测不到才"自动下载"（官方 API 查版本 → 多镜像回退 → 断网用内置版本表）。
    不依赖 Python，不需要管理员权限，全程用户级安装。
.PARAMETER ZipPath
    PowerShell-7.x.x-win-x64.zip 路径。不填则自动搜本地，再搜不到就自动下载。
.PARAMETER ToolsRoot
    安装根目录，默认 $env:LOCALAPPDATA\ps7-toolkit
.PARAMETER Mirror
    自定义下载镜像前缀，例如 https://mirror.example.com/。不填则用内置列表。
.PARAMETER SkipDefaults
    只装不配（不写 profile / 不改注册表 / 不建快捷方式）
.PARAMETER SkipRustTools
    只装 PowerShell 7，不装 rg/fd/fzf/bat/delta/jq
.PARAMETER Force
    即使已安装也强制重装
.PARAMETER CheckOnly
    只做体检，不做任何改动
#>
[CmdletBinding()]
param(
    [string]$ZipPath,
    [string]$ToolsRoot = (Join-Path $env:LOCALAPPDATA 'ps7-toolkit'),
    [string]$Mirror,
    [switch]$SkipDefaults,
    [switch]$SkipRustTools,
    [switch]$Force,
    [switch]$CheckOnly
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
# 5.1 下 Expand-Archive 的进度条会把屏幕刷成一片 ooooo，且模块内的函数只认全局设置
$global:ProgressPreference = 'SilentlyContinue'
$ProgressPreference = 'SilentlyContinue'

$PS7Dir   = Join-Path $ToolsRoot 'ps7'
$BinDir   = Join-Path $ToolsRoot 'bin'
$CacheDir = Join-Path $ToolsRoot '_dl'
$ScriptDir= Split-Path -Parent $MyInvocation.MyCommand.Path

# 下载镜像优先级；用户 -Mirror 会插到最前
$Mirrors = @('https://gh-proxy.com/','https://ghfast.top/','https://ghproxy.net/')
if ($Mirror) { $Mirrors = @($Mirror) + $Mirrors }
# 微软官方短链（最终兜底，会 302 到 GitHub）
$OfficialLinks = @(
  'https://aka.ms/powershell-release?tag=stable&os=win&arch=x64',
  'https://aka.ms/powershell-lts?os=win&arch=x64'
)

# 内置版本表（断网 / API 不可用时兜底）
# tag 与 asset 必须写「真实的 release tag / 资源文件名」，不能由 pattern 猜：
#   ripgrep 的 tag 是 15.2.0（无 v）、资源叫 ripgrep-15.2.0-...zip；jq 的 tag 是 jq-1.8.2。
# 之前只存 ver，GitHub API 被限流回落时拼出的地址全 404，工具会被静默跳过。
$FALLBACK_PS7 = '7.6.7'
$CANDIDATE_PS7_VERSIONS = @('7.6.7','7.6.6','7.6.0','7.5.4','7.5.2','7.4.7','7.4.6','7.4.1','7.3.3')
$RustTools = @(
  @{ name='rg';    repo='BurntSushi/ripgrep'; tag='15.2.0';   pattern='x86_64-pc-windows-msvc.zip'; exe='rg.exe';    ver='15.2.0'; asset='ripgrep-15.2.0-x86_64-pc-windows-msvc.zip' },
  @{ name='fd';    repo='sharkdp/fd';         tag='v10.5.0';  pattern='x86_64-pc-windows-msvc.zip'; exe='fd.exe';    ver='10.5.0'; asset='fd-v10.5.0-x86_64-pc-windows-msvc.zip' },
  @{ name='fzf';   repo='junegunn/fzf';       tag='v0.74.5';  pattern='windows_amd64.zip';         exe='fzf.exe';   ver='0.74.5'; asset='fzf-0.74.5-windows_amd64.zip' },
  @{ name='bat';   repo='sharkdp/bat';        tag='v0.26.1';  pattern='x86_64-pc-windows-msvc.zip'; exe='bat.exe';   ver='0.26.1'; asset='bat-v0.26.1-x86_64-pc-windows-msvc.zip' },
  @{ name='delta'; repo='dandavison/delta';   tag='0.20.1';   pattern='x86_64-pc-windows-msvc.zip'; exe='delta.exe'; ver='0.20.1'; asset='delta-0.20.1-x86_64-pc-windows-msvc.zip' },
  @{ name='jq';    repo='jqlang/jq';          tag='jq-1.8.2'; pattern='jq-windows-amd64.exe';      exe='jq.exe';    ver='1.8.2';  asset='jq-windows-amd64.exe' }
)

function Write-Step($m) { Write-Host "`n==> $m" -ForegroundColor Cyan }
function Write-Ok   ($m) { Write-Host "    [OK] $m" -ForegroundColor Green }
function Write-Warn ($m) { Write-Host "    [!]  $m" -ForegroundColor Yellow }
function Write-Err  ($m) { Write-Host "    [X]  $m" -ForegroundColor Red }
function Write-Info ($m) { Write-Host "    - $m" -ForegroundColor DarkGray }

# ------------------------------------------------ 探测已安装的 pwsh
function Find-ExistingPwsh {
    $cands = @(
        (Join-Path $PS7Dir 'pwsh.exe'),
        'C:\Program Files\PowerShell\7\pwsh.exe',
        'C:\Program Files\PowerShell\7-preview\pwsh.exe',
        (Join-Path $env:LOCALAPPDATA 'Programs\PowerShell\7\pwsh.exe'),
        (Join-Path $env:LOCALAPPDATA 'Microsoft\WindowsApps\pwsh.exe'),
        (Join-Path $env:USERPROFILE 'scoop\apps\powershell\current\pwsh.exe'),
        'C:\ProgramData\chocolatey\bin\pwsh.exe'
    )
    foreach ($k in @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe',
                     'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe')) {
        if (Test-Path $k) {
            $v = (Get-ItemProperty $k -ErrorAction SilentlyContinue).'(default)'
            if ($v) { $cands += $v }
        }
    }
    $g = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($g) { $cands += $g.Source }
    foreach ($c in ($cands | Where-Object { $_ } | Select-Object -Unique)) {
        if (Test-Path $c) {
            try {
                $v = & $c -NoProfile -Command '$PSVersionTable.PSVersion.Major' 2>$null | Select-Object -First 1
                if ([int]$v -ge 7) { return $c }
            } catch { }
        }
    }
    return $null
}

function Find-ExistingRustTool {
    param([string]$Name)
    $local = Join-Path $BinDir "$Name.exe"
    if (Test-Path $local) { return $local }
    $g = Get-Command $Name -ErrorAction SilentlyContinue
    if ($g -and $g.Source -and ($g.Source -like '*.exe')) { return $g.Source }
    return $null
}

# ------------------------------------------------ 下载
function Invoke-Download {
    param([string]$Url, [string]$Dest)
    $urls = @()
    foreach ($m in $Mirrors) { $urls += ($m + $Url) }
    $urls += $Url
    foreach ($u in $urls) {
        Write-Info "试源: $u"
        & curl.exe -sL --retry 2 --connect-timeout 20 --max-time 900 -o $Dest $u 2>$null
        if ((Test-Path $Dest) -and ((Get-Item $Dest).Length -gt 10000)) { return $true }
        if (Test-Path $Dest) { Remove-Item $Dest -Force -ErrorAction SilentlyContinue }
    }
    return $false
}

function Get-LatestTag {
    param([string]$Repo)
    try {
        $r = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/latest" `
             -Headers @{ 'User-Agent'='ps7-toolkit' } -TimeoutSec 25
        return $r.tag_name
    } catch { return $null }
}

# 通过 GitHub API 找到真实的资源文件名与下载地址（asset 名不能靠猜，
# 例如 ripgrep 的 asset 是 ripgrep-15.2.0-x86_64-pc-windows-msvc.zip）
function Resolve-ReleaseAssetUrl {
    param([string]$Repo, [string]$Tag, [string]$Pattern, [string]$FallbackAsset)
    try {
        $r = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/tags/$Tag" `
             -Headers @{ 'User-Agent'='ps7-toolkit' } -TimeoutSec 25
        $a = $r.assets | Where-Object {
            $_.name -like "*$Pattern*" -and $_.name -notmatch '\.(sha256|sig|asc)$'
        } | Select-Object -First 1
        if ($a) { return $a.browser_download_url }
    } catch { }
    # API 不可用（限流/断网）：用内置表里的真实资源名拼，别拿 pattern 猜
    $name = if ($FallbackAsset) { $FallbackAsset } else { $Pattern }
    return "https://github.com/$Repo/releases/download/$Tag/$name"
}

# 依次 HEAD 探测候选版本，返回第一个存在的 zip URL
function Resolve-Ps7UrlByProbe {
    foreach ($v in $CANDIDATE_PS7_VERSIONS) {
        $u = "https://github.com/PowerShell/PowerShell/releases/download/v$v/PowerShell-$v-win-x64.zip"
        foreach ($m in $Mirrors) {
            $code = & curl.exe -sIL --max-time 25 -o NUL -w '%{http_code}' ($m + $u) 2>$null
            if ($code -eq '200') { return ($m + $u) }
        }
    }
    return $null
}

function Find-LocalZip {
    param([string]$Hint)
    if ($Hint) {
        if (Test-Path $Hint) { return (Resolve-Path $Hint).Path }
        # 用户明确指定了安装包，却找不到：直接失败，而不是偷偷改成联网下载
        Write-Err "-ZipPath 指定的文件不存在: $Hint"
        Write-Err '请检查路径；或去掉 -ZipPath，让安装器自动搜索/下载。'
        exit 1
    }
    $dirs = @(
        (Join-Path $env:USERPROFILE 'Downloads'), (Join-Path $env:USERPROFILE 'Desktop'),
        (Join-Path $env:USERPROFILE '下载'),      (Join-Path $env:USERPROFILE '迅雷下载'),
        (Join-Path $env:USERPROFILE 'Documents'), $env:TEMP
    )
    foreach ($d in $dirs) {
        if (Test-Path $d) {
            $hit = Get-ChildItem $d -Filter 'PowerShell-*-win-x64.zip' -File -ErrorAction SilentlyContinue |
                   Sort-Object LastWriteTime -Descending | Select-Object -First 1
            if ($hit) { return $hit.FullName }
        }
    }
    return $null
}

# ------------------------------------------------ 主流程
Write-Host "`n########## PowerShell 7 + Rust 工具链 安装器 ##########" -ForegroundColor Magenta
Write-Host "安装根目录: $ToolsRoot"

if ($CheckOnly) {
    $ex = Find-ExistingPwsh
    if ($ex) { Write-Ok "已装 PowerShell 7: $ex  ($(& $ex -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'))" }
    else { Write-Warn '未发现 PowerShell 7' }
    $v = Join-Path $ScriptDir 'verify.ps1'
    if (Test-Path $v) { & $v -ToolsRoot $ToolsRoot }
    exit 0
}

New-Item -ItemType Directory -Force -Path $ToolsRoot, $BinDir, $CacheDir | Out-Null

# ---- 1. PowerShell 7：探测优先，其次本地 zip，最后自动下载 ----
$PwshExe  = $null
$Existing = $null
if (-not $Force) {
    Write-Step '探测已安装的 PowerShell 7'
    $PwshExe = Find-ExistingPwsh
    if ($PwshExe) {
        Write-Ok "发现已安装版本，直接复用: $PwshExe ($(& $PwshExe -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'))"
        if (-not (Test-Path (Join-Path $PS7Dir 'pwsh.exe'))) {
            Write-Info "未复制到 $PS7Dir —— 沿用系统已有安装，不额外占用磁盘。"
            Write-Info "要让 pwsh 也放进这个目录，请加 -Force 重新执行（会从本机已有安装复制，不联网）。"
        }
    } else { Write-Info '未发现，开始下载' }
} else {
    Write-Step '强制重装模式'
    $Existing = Find-ExistingPwsh
}

if (-not $PwshExe -and $Existing) {
    # -Force 且本机已有安装：复制一份到 -ToolsRoot，实现真正「搬到别的盘 / 自包含」，不联网下载
    $srcDir = Split-Path -Parent $Existing
    Write-Step "从本机已有安装复制到 $PS7Dir（不联网）"
    Write-Info "来源: $srcDir"
    if (Test-Path $PS7Dir) { Remove-Item $PS7Dir -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $PS7Dir | Out-Null
    Copy-Item (Join-Path $srcDir '*') $PS7Dir -Recurse -Force
    $PwshExe = Join-Path $PS7Dir 'pwsh.exe'
    if (-not (Test-Path $PwshExe)) {
        Write-Warn '复制失败，改为下载安装'
        $PwshExe = $null
    } else {
        Write-Ok "复制完成: $(& $PwshExe -NoProfile -Command '$PSVersionTable.PSVersion.ToString()')"
    }
}

if (-not $PwshExe) {
    Write-Step '准备安装包'
    $zip = Find-LocalZip -Hint $ZipPath
    if ($zip) { Write-Ok "使用本地安装包: $zip" }
    else {
        Write-Step '自动下载 PowerShell 7'
        $tag = Get-LatestTag -Repo 'PowerShell/PowerShell'
        $dlUrl = $null
        if ($tag) {
            $v = $tag.TrimStart('v')
            Write-Info "官方最新版本: $v"
            $dlUrl = "https://github.com/PowerShell/PowerShell/releases/download/$tag/PowerShell-$v-win-x64.zip"
        } else {
            Write-Warn 'GitHub API 不可用，改用候选版本逐个探测'
            $dlUrl = Resolve-Ps7UrlByProbe
        }
        $zip = Join-Path $CacheDir 'ps7.zip'
        $ok = $false
        if ($dlUrl) { $ok = Invoke-Download -Url $dlUrl -Dest $zip }
        if (-not $ok) {
            Write-Warn '镜像源失败，改试微软官方短链'
            foreach ($l in $OfficialLinks) {
                & curl.exe -sL --retry 1 --connect-timeout 20 --max-time 900 -o $zip $l 2>$null
                if ((Test-Path $zip) -and ((Get-Item $zip).Length -gt 100000)) { $ok = $true; break }
            }
        }
        if (-not $ok) {
            $fb = "https://github.com/PowerShell/PowerShell/releases/download/v$FALLBACK_PS7/PowerShell-$FALLBACK_PS7-win-x64.zip"
            Write-Warn "再试内置兜底版本 $FALLBACK_PS7"
            $ok = Invoke-Download -Url $fb -Dest $zip
        }
        if (-not $ok) {
            Write-Err '全部下载源都失败。请手动下载后重跑并加 -ZipPath <路径>'
            Write-Err '下载地址: https://github.com/PowerShell/PowerShell/releases/latest'
            exit 1
        }
        Write-Ok "下载完成 ($([math]::Round((Get-Item $zip).Length/1MB,1)) MB)"
    }
    if (Test-Path $PS7Dir) { Remove-Item $PS7Dir -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $PS7Dir | Out-Null
    Write-Step '解压中（30~90 秒，请耐心）'
    Expand-Archive -Path $zip -DestinationPath $PS7Dir -Force
    $PwshExe = Join-Path $PS7Dir 'pwsh.exe'
    if (-not (Test-Path $PwshExe)) { Write-Err '解压后未找到 pwsh.exe，压缩包可能损坏'; exit 1 }
    Write-Ok "安装成功: $(& $PwshExe -NoProfile -Command '$PSVersionTable.PSVersion.ToString()')"
}

# ---- 2. Rust 工具：探测优先 ----
if (-not $SkipRustTools) {
    Write-Step 'Rust 高性能命令行工具'
    foreach ($t in $RustTools) {
        $exe = Join-Path $BinDir $t.exe
        $reused = $false
        if (-not $Force) {
            $found = Find-ExistingRustTool -Name $t.name
            if ($found) {
                if ($found -eq $exe) {
                    Write-Ok "$($t.name) 已存在，跳过"
                    $reused = $true
                } else {
                    try {
                        Copy-Item $found $exe -Force
                        # 必须验一下：chocolatey/scoop 装的可能是 shim，
                        # 单文件复制出去后会找不到真正的 exe（'Cannot find file at ..\lib\...'）
                        $probe = (& $exe --version 2>&1 | Out-String)
                        if ($LASTEXITCODE -ne 0 -or -not $probe.Trim()) { throw 'no version output' }
                        Write-Ok "$($t.name) 已存在(来自 $found)，已复制到 $BinDir"
                        $reused = $true
                    } catch {
                        Write-Warn "$($t.name) 复用 $found 失败（可能是 shim），改为下载安装"
                        Remove-Item $exe -Force -ErrorAction SilentlyContinue
                    }
                }
                if ($reused) { continue }
            }
        }
        $tag = Get-LatestTag -Repo $t.repo
        if (-not $tag) {
            $tag = $t.tag
            Write-Info "$($t.name)：GitHub API 不可用，改用内置版本 $tag"
        }
        $url = Resolve-ReleaseAssetUrl -Repo $t.repo -Tag $tag -Pattern $t.pattern -FallbackAsset $t.asset
        $dest = Join-Path $CacheDir ([System.IO.Path]::GetFileName($url))
        if (-not (Invoke-Download -Url $url -Dest $dest)) { Write-Warn "$($t.name) 下载失败，跳过"; continue }
        try {
            if ($t.pattern -like '*.zip') {
                $tmp = Join-Path $CacheDir "$($t.name)_x"
                if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
                Expand-Archive -Path $dest -DestinationPath $tmp -Force
                $f = Get-ChildItem $tmp -Recurse -Filter $t.exe -File | Select-Object -First 1
                if ($f) { Copy-Item $f.FullName $exe -Force; Write-Ok "$($t.name) -> $exe" }
                else { Write-Warn "$($t.name) 压缩包内未找到 $($t.exe)" }
            } else {
                Copy-Item $dest $exe -Force
                Write-Ok "$($t.name) -> $exe"
            }
        } catch { Write-Warn "$($t.name) 安装异常: $($_.Exception.Message)" }
    }
}

# ---- 3. 默认化 ----
if (-not $SkipDefaults) {
    Write-Step '配置系统默认（profile / 注册表 / 文件关联 / 快捷方式 / 终端 / VSCode）'
    $setup = Join-Path $ScriptDir 'setup-defaults.ps1'
    if (Test-Path $setup) { & $setup -PwshPath $PwshExe -BinDir $BinDir }
    else { Write-Warn '找不到 setup-defaults.ps1，跳过默认化' }
}

# ---- 4. 清理下载缓存（装完就没用了，别留 100MB 垃圾） ----
# 注意：这个目录在开头就无条件建了出来，即使全程复用系统已装的工具、一个字节都没下，
# 也会留下一个空目录。所以判断条件必须是「目录存在就删」，不能是「有文件才删」
# —— 没有文件时 Measure-Object 的 Sum 是 $null，$null -gt 0 恒为假，空目录永远清不掉。
if (Test-Path $CacheDir) {
    $freed = 0
    try {
        $m = Get-ChildItem $CacheDir -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum
        if ($m -and $m.Sum) { $freed = [double]$m.Sum }
    } catch { }
    Remove-Item $CacheDir -Recurse -Force -ErrorAction SilentlyContinue
    if (Test-Path $CacheDir) {
        Write-Warn "下载缓存没能删干净（可能被占用），可手动删除: $CacheDir"
    } elseif ($freed -gt 0) {
        Write-Step ("清理下载缓存，释放约 {0} MB" -f [math]::Round($freed / 1MB, 1))
    } else {
        Write-Step '清理下载缓存（没有实际下载，仅删掉空目录）'
    }
}

# ---- 5. 体检 ----
$verify = Join-Path $ScriptDir 'verify.ps1'
if (Test-Path $verify) {
    $vargs = @{ ToolsRoot = $ToolsRoot; PwshPath = $PwshExe; BinDir = $BinDir }
    if ($SkipDefaults) { $vargs['SkipDefaults'] = $true }
    & $verify @vargs
}

Write-Host "`n########## 完成 ##########" -ForegroundColor Magenta
Write-Host "PowerShell 7 : $PwshExe"
Write-Host "Rust 工具    : $BinDir"
Write-Host "立即试用     : & '$PwshExe' -NoProfile -Command '`$PSVersionTable.PSVersion'"
Write-Host "提示: 重新打开终端/应用后 PATH 才生效`n"
exit 0
