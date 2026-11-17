<#
.SYNOPSIS
    Smoke test for HermesClawZero Auto Memory skill.
.DESCRIPTION
    Verifies: memory initialization, Sidecar connectivity, capture, search, and error handling.
#>

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$memPy = Join-Path $scriptDir "memory.py"
$passed = 0
$failed = 0

function Test-Step {
    param($Name, $ScriptBlock)
    try {
        & $ScriptBlock
        Write-Host "  ✓ $Name" -ForegroundColor Green
        $script:passed++
    } catch {
        Write-Host "  ✗ $Name : $_" -ForegroundColor Red
        $script:failed++
    }
}

Write-Host "🧪 HermesClawZero Auto Memory — Smoke Test" -ForegroundColor Cyan
Write-Host ""

# 1. Script exists
Test-Step "memory.py exists" {
    if (-not (Test-Path $memPy)) { throw "memory.py not found at $memPy" }
}

# 2. Python syntax valid
Test-Step "Python syntax" {
    python -m py_compile $memPy 2>&1 | Out-Null
}

# 3. Sidecar reachable
Test-Step "Sidecar reachable" {
    $r = python "$memPy" search "smoke-test-init" 1 2>&1
    if ($LASTEXITCODE -gt 1) { throw "Sidecar unreachable: $r" }
}

# 4. Capture memory
Test-Step "Capture memory" {
    $r = python "$memPy" capture "Smoke test $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "smoke_test" 2>&1
    $json = $r | ConvertFrom-Json 2>$null
    if (-not $json -or $json.status -ne "ok") { throw "Capture failed: $r" }
}

# 5. Search memory
Test-Step "Search memory" {
    $r = python "$memPy" search "smoke test" 2 2>&1
    if ($LASTEXITCODE -gt 0) { throw "Search failed: $r" }
}

# 6. Empty capture (error case)
Test-Step "Empty capture rejected" {
    $r = python "$memPy" capture "" 2>&1
    if ($LASTEXITCODE -eq 0) { throw "Empty capture should fail" }
}

# 7. Autosave
Test-Step "Autosave" {
    $r = python "$memPy" autosave "Smoke test autosave $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "smoke_test_backup.md" 2>&1
    $json = $r | ConvertFrom-Json 2>$null
    if (-not $json -or $json.status -ne "ok") { throw "Autosave failed: $r" }
}

# 8. Help output
Test-Step "Help output" {
    $r = python "$memPy" 2>&1
    if ($r -notmatch "capture|search|autosave") { throw "Help missing commands" }
}

Write-Host ""
Write-Host "Results: $passed passed, $failed failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
exit $failed
