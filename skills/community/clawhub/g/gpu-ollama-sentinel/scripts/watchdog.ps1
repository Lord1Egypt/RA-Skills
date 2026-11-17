# GPU / Ollama Sentinel watchdog (single file, no dependencies)
# Checks Ollama API + GPU state; heals Ollama if dead; appends JSONL log.
# All ASCII-only output to avoid codepage corruption on Windows consoles.
param(
    [string]$OllamaUrl = "http://127.0.0.1:11434",
    [int]$MinFreeVramMB = 1500,          # below this AND util~=0 => suspect stuck
    [string]$HealCommand = "ollama serve",  # command used to restart Ollama
    [string]$LogFile = "$PSScriptRoot\sentinel-log.jsonl",
    [switch]$NoHeal                      # observe-only mode
)
$ErrorActionPreference = 'SilentlyContinue'
$result = [ordered]@{
    ts = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
    ollama = 'up'; models = 0; action = 'none'; result = ''
    gpu_free_mb = $null; gpu_util_pct = $null; suspect = ''
}

# --- 1. Ollama health ---
$sw = [Diagnostics.Stopwatch]::StartNew()
try {
    $resp = Invoke-RestMethod -Uri "$OllamaUrl/api/tags" -TimeoutSec 5
    $sw.Stop()
    $result.models = @($resp.models).Count
} catch {
    $sw.Stop()
    $result.ollama = 'down'
    if ($NoHeal) {
        $result.action = 'would_restart_ollama'; $result.result = 'observe-only'
    } else {
        $result.action = 'restart_ollama'
        $exe = (Get-Command ollama -ErrorAction SilentlyContinue).Source
        if (-not $exe) { $exe = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" }
        if ($exe) {
            Start-Process -FilePath $exe -ArgumentList 'serve' -WindowStyle Hidden
            Start-Sleep -Seconds 6
            $probe = $null
            try { $probe = Invoke-RestMethod -Uri "$OllamaUrl/api/tags" -TimeoutSec 5 } catch {}
            if ($probe) { $result.result = 'healed' } else { $result.result = 'heal_failed' }
        } else { $result.result = 'ollama_exe_not_found' }
    }
}

# --- 2. GPU state (nvidia-smi; absent is fine, CPU boxes supported) ---
$smi = (Get-Command nvidia-smi -ErrorAction SilentlyContinue).Source
if (-not $smi) { $smi = "$env:SystemRoot\System32\nvidia-smi.exe" }
if (Test-Path $smi) {
    $raw = & $smi --query-gpu=memory.free,utilization.gpu --format=csv,noheader,nounits 2>$null
    if ($raw) {
        $p = ($raw -split ",\s*") | ForEach-Object { [int]($_ -replace '[^0-9]','') }
        $result.gpu_free_mb = $p[0]; $result.gpu_util_pct = $p[1]
        if ($p[0] -lt $MinFreeVramMB -and $p[1] -le 2) {
            $result.suspect = 'vram_hoarding_idle_gpu'
            # evidence, not execution: list top VRAM processes for human review
            $procs = & $smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader 2>$null
            if ($procs) { $result.suspect += ' | procs: ' + ($procs -join ' ; ') }
        }
    }
} else { $result.suspect = 'nvidia_smi_not_found' }

# --- 3. append JSONL log ---
($result | ConvertTo-Json -Compress) | Add-Content -Path $LogFile -Encoding utf8

# --- 4. console verdict (human-friendly) ---
$verdict = if ($result.ollama -eq 'up' -and -not $result.suspect) { 'HEALTHY' }
           elseif ($result.action -like 'restart*') { "ACTION: $($result.action) => $($result.result)" }
           else { "ATTENTION: $($result.suspect)" }
Write-Output "[$($result.ts)] $verdict (models=$($result.models), free_vram=$($result.gpu_free_mb)MB, util=$($result.gpu_util_pct)%)"
