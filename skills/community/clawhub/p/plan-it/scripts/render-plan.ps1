# render-plan.ps1 — open plan.html in the default browser (Windows).

$ErrorActionPreference = "Stop"

function Resolve-PlanPath {
    if ($env:PLAN_ID) {
        $cand = Join-Path ".planning" (Join-Path $env:PLAN_ID "plan.html")
        if (Test-Path $cand) { return $cand }
    }
    if ($env:CLAUDE_PLUGIN_ROOT) { } # no-op, kept for parity with bash script env handling
    if (Test-Path ".planning\.active_plan") {
        $ap = (Get-Content -Raw ".planning\.active_plan").Trim()
        if ($ap) {
            $cand = Join-Path ".planning" (Join-Path $ap "plan.html")
            if (Test-Path $cand) { return $cand }
        }
    }
    if (Test-Path "plan.html") { return "plan.html" }
    return $null
}

$PlanPath = Resolve-PlanPath
if (-not $PlanPath) {
    Write-Error "[plan-it] no plan.html found. Run: pwsh scripts\init-plan.ps1 <template>"
    exit 1
}

$Abs = (Resolve-Path $PlanPath).Path
Start-Process $Abs
Write-Host "[plan-it] opened $Abs"
