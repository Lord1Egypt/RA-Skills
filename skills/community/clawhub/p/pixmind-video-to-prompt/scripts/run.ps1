param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$ScriptArguments
)

$ErrorActionPreference = 'Stop'
$RequiredVersion = '24.20.0'
$Architecture = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { 'arm64' } else { 'x64' }
$ManifestUrl = if ($env:PIXMIND_NODE_MANIFEST) {
  $env:PIXMIND_NODE_MANIFEST
} else {
  "https://cdn.pixmind.io/pixmind-builder/dependencies/node/windows/$Architecture/manifest.json"
}
$FallbackSha256 = if ($Architecture -eq 'arm64') {
  '92949e7764e56e305cb84ea3d575912e822c79e85599362e8d408b04b9ffd326'
} else {
  '5c976096e04e5c2c1f091938926234cc9fbebfe9787ddd149351b3b0ecc707b5'
}
$Fallback = [pscustomobject]@{
  version = $RequiredVersion
  url = $null
  size = 0
  sha256 = $FallbackSha256
  officialUrl = "https://nodejs.org/dist/v$RequiredVersion/win-$Architecture/node.exe"
  officialSha256 = $FallbackSha256
}

function Invoke-VideoToPrompt([string]$NodePath) {
  & $NodePath (Join-Path $PSScriptRoot 'video-to-prompt.js') @ScriptArguments
  exit $LASTEXITCODE
}

function Test-NodeRuntime($File, $Version, $Size, $Sha256) {
  if (!(Test-Path -LiteralPath $File -PathType Leaf)) { return $false }
  if ($Size -and (Get-Item -LiteralPath $File).Length -ne [long]$Size) { return $false }
  if ($Sha256 -and (Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Sha256.ToLowerInvariant()) {
    return $false
  }
  try {
    return (& $File --version 2>$null) -eq "v$Version"
  } catch {
    return $false
  }
}

function Save-VerifiedRuntime($Source, $Destination, $Version, $Size, $Sha256) {
  if (!$Source) { return $false }
  $Temporary = "$Destination.$PID.download.exe"
  try {
    Invoke-WebRequest -UseBasicParsing -Uri $Source -OutFile $Temporary -TimeoutSec 900
    if (!(Test-NodeRuntime $Temporary $Version $Size $Sha256)) {
      throw "Node.js download failed size, SHA-256, or version validation: $Source"
    }
    Move-Item -LiteralPath $Temporary -Destination $Destination -Force
    return $true
  } catch {
    Write-Warning $_.Exception.Message
    return $false
  } finally {
    Remove-Item -LiteralPath $Temporary -Force -ErrorAction SilentlyContinue
  }
}

if (!$env:PIXMIND_NODE_FORCE_PORTABLE) {
  $SystemNode = Get-Command node -ErrorAction SilentlyContinue
  if ($SystemNode) { Invoke-VideoToPrompt $SystemNode.Source }
}

$Entry = $Fallback
try {
  $Manifest = Invoke-RestMethod -UseBasicParsing -Uri $ManifestUrl -TimeoutSec 30
  $Selected = @($Manifest.versions) | Where-Object { $_.version -eq $Manifest.preferred } | Select-Object -First 1
  if (!$Selected) { $Selected = @($Manifest.versions) | Select-Object -First 1 }
  if ($Selected) { $Entry = $Selected }
} catch {
  Write-Warning "Pixmind Node.js manifest is unavailable; using the nodejs.org fallback. $($_.Exception.Message)"
}

$CacheRoot = if ($env:PIXMIND_CACHE_DIR) {
  $env:PIXMIND_CACHE_DIR
} elseif ($env:LOCALAPPDATA) {
  Join-Path $env:LOCALAPPDATA 'Pixmind\cache'
} else {
  Join-Path ([Environment]::GetFolderPath('LocalApplicationData')) 'Pixmind\cache'
}
$Directory = Join-Path $CacheRoot "node\windows-$Architecture\$($Entry.version)"
$Node = Join-Path $Directory 'node.exe'
New-Item -ItemType Directory -Path $Directory -Force | Out-Null

if (Test-NodeRuntime $Node $Entry.version $Entry.size $Entry.sha256) { Invoke-VideoToPrompt $Node }
if (Save-VerifiedRuntime $Entry.url $Node $Entry.version $Entry.size $Entry.sha256) { Invoke-VideoToPrompt $Node }

$OfficialSha256 = if ($Entry.officialSha256) { $Entry.officialSha256 } else { $Fallback.officialSha256 }
if (Save-VerifiedRuntime $Entry.officialUrl $Node $Entry.version 0 $OfficialSha256) { Invoke-VideoToPrompt $Node }

throw @"
Unable to install the portable Pixmind Node.js runtime.
Official Node.js download: https://nodejs.org/en/download
Backup command shown by the official download flow:
  winget install OpenJS.NodeJS.LTS
After installation, open a new terminal and retry.
"@
