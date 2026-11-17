param(
  [switch]$PrintNode,
  [switch]$Ensure,
  [switch]$Check
)

$ErrorActionPreference = 'Stop'
$MinimumMajor = if ($env:HAOLVSHI_NODE_MIN_MAJOR) { [int]$env:HAOLVSHI_NODE_MIN_MAJOR } elseif ($env:LVPIN_NODE_MIN_MAJOR) { [int]$env:LVPIN_NODE_MIN_MAJOR } else { 20 }
$ReleaseLine = if ($env:HAOLVSHI_NODE_RELEASE_LINE) { [int]$env:HAOLVSHI_NODE_RELEASE_LINE } elseif ($env:LVPIN_NODE_RELEASE_LINE) { [int]$env:LVPIN_NODE_RELEASE_LINE } else { 22 }

if ($env:HAOLVSHI_RUNTIME_DIR) {
  $RuntimeRoot = $env:HAOLVSHI_RUNTIME_DIR
} elseif ($env:LVPIN_RUNTIME_DIR) {
  $RuntimeRoot = $env:LVPIN_RUNTIME_DIR
} elseif ($env:LOCALAPPDATA) {
  $RuntimeRoot = Join-Path $env:LOCALAPPDATA 'haolvshi-legal-skill\runtime'
} else {
  $RuntimeRoot = Join-Path $env:USERPROFILE '.local\share\haolvshi-legal-skill\runtime'
}
$LegacyRuntimeRoot = if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'lvpin-legal-skill\runtime' } else { Join-Path $env:USERPROFILE '.local\share\lvpin-legal-skill\runtime' }
$NodePathFile = Join-Path $RuntimeRoot 'node-path'
$LegacyNodePathFile = Join-Path $LegacyRuntimeRoot 'node-path'

function Test-CompatibleNode([string]$Candidate) {
  if (-not $Candidate -or -not (Test-Path -LiteralPath $Candidate -PathType Leaf)) { return $false }
  try {
    $Version = (& $Candidate --version 2>$null).Trim()
    return [int]($Version -replace '^v([0-9]+).*$', '$1') -ge $MinimumMajor
  } catch {
    return $false
  }
}

function Resolve-Node {
  if (Test-CompatibleNode $env:HAOLVSHI_NODE_BIN) { return $env:HAOLVSHI_NODE_BIN }
  if (Test-CompatibleNode $env:LVPIN_NODE_BIN) { return $env:LVPIN_NODE_BIN }
  $SystemNode = Get-Command node -ErrorAction SilentlyContinue
  if ($SystemNode -and (Test-CompatibleNode $SystemNode.Source)) { return $SystemNode.Source }
  if (Test-Path -LiteralPath $NodePathFile) {
    $CachedNode = (Get-Content -LiteralPath $NodePathFile -TotalCount 1).Trim()
    if (Test-CompatibleNode $CachedNode) { return $CachedNode }
  }
  if (Test-Path -LiteralPath $LegacyNodePathFile) {
    $CachedNode = (Get-Content -LiteralPath $LegacyNodePathFile -TotalCount 1).Trim()
    if (Test-CompatibleNode $CachedNode) { return $CachedNode }
  }
  return $null
}

function Install-Node {
  $Architecture = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString().ToLowerInvariant()
  if ($Architecture -notin @('x64', 'arm64')) {
    throw "暂不支持自动安装到 $Architecture 架构，请手动安装 Node.js $MinimumMajor 以上版本。"
  }

  [Console]::Error.WriteLine("未检测到 Node.js $MinimumMajor 以上版本，正在从 Node.js 官方站点安装独立运行环境。")
  $ReleaseUrl = "https://nodejs.org/dist/latest-v$ReleaseLine.x"
  $TemporaryDir = Join-Path ([System.IO.Path]::GetTempPath()) ("haolvshi-node-" + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $TemporaryDir -Force | Out-Null
  try {
    $ManifestPath = Join-Path $TemporaryDir 'SHASUMS256.txt'
    Invoke-WebRequest -UseBasicParsing -Uri "$ReleaseUrl/SHASUMS256.txt" -OutFile $ManifestPath
    $Pattern = "^(?<hash>[0-9a-f]{64})\s+(?<file>node-v.+-win-$Architecture\.zip)$"
    $Match = Get-Content -LiteralPath $ManifestPath | ForEach-Object {
      if ($_ -match $Pattern) { [pscustomobject]@{ Hash = $Matches.hash; File = $Matches.file } }
    } | Select-Object -First 1
    if (-not $Match) { throw 'Node.js 官方清单中没有找到适合当前系统的安装包。' }

    $ArchivePath = Join-Path $TemporaryDir $Match.File
    Invoke-WebRequest -UseBasicParsing -Uri "$ReleaseUrl/$($Match.File)" -OutFile $ArchivePath
    $ActualHash = (Get-FileHash -LiteralPath $ArchivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($ActualHash -ne $Match.Hash.ToLowerInvariant()) { throw 'Node.js 安装包校验失败，已停止安装。' }

    $ExtractPath = Join-Path $TemporaryDir 'extracted'
    Expand-Archive -LiteralPath $ArchivePath -DestinationPath $ExtractPath -Force
    $VersionsRoot = Join-Path $RuntimeRoot 'versions'
    New-Item -ItemType Directory -Path $VersionsRoot -Force | Out-Null
    $ExtractedName = [System.IO.Path]::GetFileNameWithoutExtension($Match.File)
    $InstallDir = Join-Path $VersionsRoot $ExtractedName
    if (-not (Test-Path -LiteralPath $InstallDir)) {
      Move-Item -LiteralPath (Join-Path $ExtractPath $ExtractedName) -Destination $InstallDir
    }
    $InstalledNode = Join-Path $InstallDir 'node.exe'
    if (-not (Test-CompatibleNode $InstalledNode)) { throw 'Node.js 运行环境安装后验证失败。' }
    Set-Content -LiteralPath $NodePathFile -Value $InstalledNode -Encoding UTF8
    return $InstalledNode
  } finally {
    Remove-Item -LiteralPath $TemporaryDir -Recurse -Force -ErrorAction SilentlyContinue
  }
}

$Installed = $false
$NodeBin = Resolve-Node
if (-not $NodeBin) {
  $NodeBin = Install-Node
  $Installed = $true
}

if ($PrintNode) {
  Write-Output $NodeBin
} else {
  [pscustomobject]@{
    ok = $true
    stage = 'environment_ready'
    installed = $Installed
    nodePath = $NodeBin
    nodeVersion = (& $NodeBin --version).Trim()
  } | ConvertTo-Json -Compress
}
