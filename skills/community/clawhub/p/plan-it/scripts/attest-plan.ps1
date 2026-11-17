# attest-plan.ps1 — compute SHA-256 of active plan.html and store it (Windows).
#
# Usage:
#   .\attest-plan.ps1            # compute and store
#   .\attest-plan.ps1 -Show      # print stored hash
#   .\attest-plan.ps1 -Clear     # delete attestation

param(
    [switch]$Show,
    [switch]$Clear
)

$ErrorActionPreference = "Stop"

function Resolve-PlanAndAttest {
    if ($env:PLAN_ID) {
        $cand = Join-Path ".planning" (Join-Path $env:PLAN_ID "plan.html")
        if (Test-Path $cand) {
            return @{ Plan = $cand; Attest = (Join-Path ".planning" (Join-Path $env:PLAN_ID ".attestation")) }
        }
    }
    if (Test-Path ".planning\.active_plan") {
        $ap = (Get-Content -Raw ".planning\.active_plan").Trim()
        if ($ap) {
            $cand = Join-Path ".planning" (Join-Path $ap "plan.html")
            if (Test-Path $cand) {
                return @{ Plan = $cand; Attest = (Join-Path ".planning" (Join-Path $ap ".attestation")) }
            }
        }
    }
    if (Test-Path "plan.html") {
        return @{ Plan = "plan.html"; Attest = ".plan-attestation" }
    }
    return $null
}

$Resolved = Resolve-PlanAndAttest
if (-not $Resolved) {
    Write-Error "[plan-it] no plan.html found. Run: pwsh scripts\init-plan.ps1 <template>"
    exit 1
}

$PlanPath = $Resolved.Plan
$AttestPath = $Resolved.Attest

if ($Show) {
    if (Test-Path $AttestPath) {
        (Get-Content -Raw $AttestPath).Trim()
    } else {
        Write-Error "[plan-it] no attestation found at $AttestPath"
        exit 2
    }
    return
}

if ($Clear) {
    if (Test-Path $AttestPath) {
        Remove-Item -Force $AttestPath
        Write-Host "[plan-it] attestation cleared at $AttestPath"
    } else {
        Write-Host "[plan-it] no attestation to clear at $AttestPath"
    }
    return
}

# v0.2.0: write the browser-verifiable content seal into the plan-data JSON
# BEFORE hashing, so the whole-file attestation covers the sealed file. Best
# effort: missing Python falls back to whole-file-only attestation. Probe-execute
# each candidate so the Windows Store python3 alias is rejected for a real one.
$Py = $null
foreach ($cand in @("python", "python3")) {
    $c = Get-Command $cand -ErrorAction SilentlyContinue
    if ($c) {
        & $c.Source -c "import sys" 2>$null
        if ($LASTEXITCODE -eq 0) { $Py = $c.Source; break }
    }
}
$Helper = Join-Path $PSScriptRoot "plan-hook.py"
if ($Py -and (Test-Path $Helper)) {
    try { & $Py $Helper seal } catch { Write-Host "[plan-it] content-seal step skipped; continuing with whole-file attestation" }
} else {
    Write-Host "[plan-it] no working Python found for content-seal; whole-file attestation only"
}

$Hash = (Get-FileHash -Path $PlanPath -Algorithm SHA256).Hash.ToLower()
$AttestDir = Split-Path -Parent $AttestPath
if ($AttestDir -and -not (Test-Path $AttestDir)) {
    New-Item -ItemType Directory -Force -Path $AttestDir | Out-Null
}
Set-Content -Path $AttestPath -Value $Hash -NoNewline
Write-Host "[plan-it] attestation stored at $AttestPath"
Write-Host "[plan-it] sha256: $Hash"
