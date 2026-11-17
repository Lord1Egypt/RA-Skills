[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$FilePath,
    [string[]]$Arguments = @(),
    [int]$TimeoutSec = 60,
    [string]$WorkingDirectory = $PWD.Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = $FilePath
$psi.WorkingDirectory = $WorkingDirectory
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true
foreach ($a in $Arguments) { $psi.ArgumentList.Add([string]$a) }

$p = [System.Diagnostics.Process]::new()
$p.StartInfo = $psi

$sw = [System.Diagnostics.Stopwatch]::StartNew()
[void]$p.Start()
$outTask = $p.StandardOutput.ReadToEndAsync()
$errTask = $p.StandardError.ReadToEndAsync()

$exited = $p.WaitForExit($TimeoutSec * 1000)
if (-not $exited) {
    try { $p.Kill($true) } catch { try { $p.Kill() } catch { } }
    $timedOut = $true
} else {
    $timedOut = $false
}
$stdout = $outTask.GetAwaiter().GetResult()
$stderr = $errTask.GetAwaiter().GetResult()
$sw.Stop()

[pscustomobject]@{
    file      = $FilePath
    args      = @($Arguments)
    exit_code = $(if ($timedOut) { $null } else { $p.ExitCode })
    timed_out = $timedOut
    seconds   = [math]::Round($sw.Elapsed.TotalSeconds, 3)
    stdout    = $stdout
    stderr    = $stderr
} | ConvertTo-Json -Depth 4
