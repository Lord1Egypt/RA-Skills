# Throttled parallel work in PowerShell 7.
# Runspaces do not share variables; pass with $using:.

param([int]$Throttle = 4, [int]$Count = 12)

$results = 1..$Count | ForEach-Object -Parallel {
    $n = $_
    Start-Sleep -Milliseconds (100 + ($n * 10))
    [pscustomobject]@{
        n       = $n
        pid     = $PID
    }
} -ThrottleLimit $Throttle

$results | Sort-Object n | Format-Table -AutoSize
