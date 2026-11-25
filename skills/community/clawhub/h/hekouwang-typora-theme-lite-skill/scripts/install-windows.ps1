<#
hekouwang · Windows installer

Usage (PowerShell):
  .\scripts\install-windows.ps1
  .\scripts\install-windows.ps1 -Paid
  .\scripts\install-windows.ps1 -FreeOnly

Default: free V2; if edition\ + paid CSS exist, also install V1–V6.
Existing theme CSS is overwritten in place; keep your own copy if you need one.
#>
[CmdletBinding()]
param(
  [string]$ThemeDir = (Join-Path $env:APPDATA 'Typora\themes'),
  [switch]$Paid,
  [switch]$FreeOnly
)

$ErrorActionPreference = 'Stop'
$slug = 'hekouwang'
$root = Split-Path -Parent $PSScriptRoot
$variants = @($slug, "${slug}-dark")
$paidVariants = @(
  'hekouwang-v1', 'hekouwang-v1-dark',
  'hekouwang-v2-pro', 'hekouwang-v2-pro-dark',
  'hekouwang-v3', 'hekouwang-v3-dark',
  'hekouwang-v4', 'hekouwang-v4-dark',
  'hekouwang-v5', 'hekouwang-v5-dark',
  'hekouwang-v6', 'hekouwang-v6-dark'
)
$legacy = @("${slug}-claude", "${slug}-claude-dark")

function Write-Ok([string]$Message) { Write-Host "  ✓ $Message" -ForegroundColor Green }
function Write-Warn([string]$Message) { Write-Host "  ! $Message" -ForegroundColor Yellow }

$installPaid = $false
if ($Paid) { $installPaid = $true }
elseif (-not $FreeOnly) {
  $edition = Join-Path $root 'edition'
  $probe = Join-Path $root 'theme\hekouwang-v1.css'
  if ((Test-Path -LiteralPath $edition -PathType Container) -and (Test-Path -LiteralPath $probe -PathType Leaf)) {
    $installPaid = $true
  }
}

if ($installPaid) {
  Write-Host 'hekouwang · install (free V2 + paid V1–V6 · Windows)'
} else {
  Write-Host 'hekouwang · install (free · V2 · Windows)'
}
Write-Host '────────────────────────────────────────'
if (-not (Test-Path -LiteralPath $ThemeDir -PathType Container)) {
  throw "Typora themes folder not found: $ThemeDir`nInstall Typora first, then use Preferences → Appearance → Open Theme Folder."
}
foreach ($variant in $variants) {
  $source = Join-Path $root "theme\$variant.css"
  if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing $source. Run: python scripts\build.py --tier free" }
}
if ($installPaid) {
  foreach ($variant in $paidVariants) {
    $source = Join-Path $root "theme\$variant.css"
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
      throw "Missing $source. Run: python scripts\build.py  (needs edition\)  or pass -FreeOnly"
    }
  }
}
foreach ($variant in $variants) {
  Copy-Item -LiteralPath (Join-Path $root "theme\$variant.css") -Destination (Join-Path $ThemeDir "$variant.css") -Force
  Write-Ok "installed $variant.css"
}
if ($installPaid) {
  foreach ($variant in $paidVariants) {
    Copy-Item -LiteralPath (Join-Path $root "theme\$variant.css") -Destination (Join-Path $ThemeDir "$variant.css") -Force
    Write-Ok "installed $variant.css"
  }
}
foreach ($variant in $legacy) {
  $current = Join-Path $ThemeDir "$variant.css"
  if (Test-Path -LiteralPath $current -PathType Leaf) { Remove-Item -LiteralPath $current -Force; Write-Ok "removed legacy $variant.css" }
}
$fontSource = Join-Path $root "theme\$slug\fonts"
$fontTarget = Join-Path $ThemeDir "$slug\fonts"
if (Test-Path -LiteralPath $fontSource -PathType Container) {
  New-Item -ItemType Directory -Force -Path $fontTarget | Out-Null
  $fonts = Get-ChildItem -LiteralPath $fontSource -File
  foreach ($font in $fonts) { Copy-Item -LiteralPath $font.FullName -Destination $fontTarget -Force }
  Write-Ok "installed $($fonts.Count) bundled Inter font file(s)"
} else { Write-Warn 'bundled fonts folder not found; Latin text will fall back to the system font' }
Write-Host '────────────────────────────────────────'
Write-Host 'Done. Quit Typora completely, reopen it, then select:'
Write-Host '  • Hekouwang / Hekouwang Dark'
if ($installPaid) {
  Write-Host '  • Hekouwang V1–V6 / V2 Pro (light + dark)'
}
Write-Host 'Changing a theme does not reload a modified CSS file; restart Typora after updates.'
