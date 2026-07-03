# LYGO Ollama Army — full capacity v3 (network-builder + mesh-cartographer)
$ErrorActionPreference = "Stop"
$ArmyRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ArmyRoot
$env:LYGO_STACK_ROOT = if ($env:LYGO_STACK_ROOT) { $env:LYGO_STACK_ROOT } else { "I:\E Drive\lygo-protocol-stack" }

Write-Host "=== LYGO Army Full Capacity v3 ===" -ForegroundColor Cyan
Write-Host "Stack root: $env:LYGO_STACK_ROOT"

# Ollama quick check
try {
    $null = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5
    Write-Host "[OK] Ollama reachable" -ForegroundColor Green
} catch {
    Write-Host "[WARN] Ollama not ready — deterministic tasks still run; LLM roles wait." -ForegroundColor Yellow
}

python -B seed_productive_tasks.py
python -B ollama_command_center\scripts\army_cron_once.py
python -B ollama_command_center\scripts\verify_army_tuning.py
python -B ollama_command_center\scripts\sentinel_heartbeat.py

Write-Host "Starting autonomous supervisor (daemons + sentinel loop + hourly cron)..." -ForegroundColor Cyan
python -B ollama_command_center\scripts\army_autonomous_supervisor.py