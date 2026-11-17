<#
.SYNOPSIS
    Install HermesClawZero Auto Memory skill.
.DESCRIPTION
    Verifies dependencies, checks Sidecar connectivity, and validates config.
#>

$ErrorActionPreference = "Stop"

Write-Host "🔌 HermesClawZero Auto Memory — Install" -ForegroundColor Cyan

# 1. Check Python
try {
    $pyVersion = python --version 2>&1
    Write-Host "  ✓ Python: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Install Python 3.10+" -ForegroundColor Red
    exit 1
}

# 2. Check requests module
try {
    python -c "import requests" 2>$null
    Write-Host "  ✓ requests module installed" -ForegroundColor Green
} catch {
    Write-Host "  Installing requests module..." -ForegroundColor Yellow
    pip install requests 2>$null
}

# 3. Check .env config
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$envPath = Join-Path $scriptDir "..\.env"
if (Test-Path $envPath) {
    Write-Host "  ✓ .env found" -ForegroundColor Green
} else {
    Write-Host "  ⚠ .env not found. Create one with API_KEY and MEM_PUBLIC_URL" -ForegroundColor Yellow
}

# 4. Test Sidecar connectivity
Write-Host "  Testing Sidecar API..." -ForegroundColor Yellow
$memPy = Join-Path $scriptDir "memory.py"
try {
    $result = python "$memPy" search "healthcheck" 1 2>&1
    Write-Host "  ✓ Sidecar API reachable" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Sidecar not reachable. Start with: docker compose up -d" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Install check complete" -ForegroundColor Cyan
