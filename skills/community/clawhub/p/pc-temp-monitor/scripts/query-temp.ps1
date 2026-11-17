#Requires -Version 5.1
[CmdletBinding()]
param(
    [string]$LHMPath = "$env:TEMP\LibreHardwareMonitor",
    [string]$OutputFile = "$env:TEMP\lhm_temps_result.txt"
)

$dll = Join-Path $LHMPath "LibreHardwareMonitorLib.dll"
if (-not (Test-Path $dll)) {
    Write-Error "LibreHardwareMonitorLib.dll not found at: $dll"
    exit 1
}

Add-Type -Path $dll
$computer = New-Object LibreHardwareMonitor.Hardware.Computer
$computer.IsCpuEnabled = $true
$computer.IsGpuEnabled = $true
$computer.Open()
Start-Sleep -Seconds 4

if (Test-Path $OutputFile) { Remove-Item $OutputFile -Force }

$lines = @()
foreach ($hardware in $computer.Hardware) {
    $hardware.Update()
    Start-Sleep -Milliseconds 300
    $hardware.Update()
    $timeStr = Get-Date -Format "yyyy/M/d HH:mm:ss"
    foreach ($sensor in $hardware.Sensors) {
        if ($sensor.SensorType -eq [LibreHardwareMonitor.Hardware.SensorType]::Temperature -and $sensor.Value -ne $null) {
            $val = $sensor.Value
            $name = "$($hardware.Name) | $($sensor.Name)"
            $lines += "$name = $val C | $timeStr"
        }
    }
}
$computer.Close()
[System.IO.File]::WriteAllLines($OutputFile, $lines, [System.Text.Encoding]::UTF8)
