<#
.SYNOPSIS
    Update HermesClawZero Auto Memory skill to the latest version.
.DESCRIPTION
    Checks GitHub for new releases and applies updates.
#>

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillDir = Resolve-Path (Join-Path $scriptDir "..")

Write-Host "🔄 HermesClawZero Auto Memory — Update Check" -ForegroundColor Cyan

# Check current version from SKILL.md
$skillMd = Join-Path $skillDir "SKILL.md"
if (Test-Path $skillMd) {
    $versionLine = Select-String -Path $skillMd -Pattern "version:" | Select-Object -First 1
    if ($versionLine) {
        $currentVersion = $versionLine.ToString() -replace '.*version:\s*"([^"]+)".*', '$1'
        Write-Host "  Current version: $currentVersion" -ForegroundColor Yellow
    }
}

# Check clawhub for latest
try {
    $latestInfo = node C:\dev\clawhub\packages\clawhub\bin\clawdhub.js skill verify hermesclawzero-auto-memory 2>&1 | ConvertFrom-Json
    Write-Host "  Latest on ClawHub: $($latestInfo.version)" -ForegroundColor Green
    Write-Host "  Page: $($latestInfo.pageUrl)" -ForegroundColor Cyan
} catch {
    Write-Host "  ⚠ Could not check ClawHub" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To update to the latest ClawHub version, re-run:"
Write-Host "  openclaw skills install hermesclawzero-auto-memory --force" -ForegroundColor Cyan
