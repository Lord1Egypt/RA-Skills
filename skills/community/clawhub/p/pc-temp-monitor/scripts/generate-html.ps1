#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    [string]$OutputFile = "$env:TEMP\temperature_report.html"
)

if (-not (Test-Path $InputFile)) {
    Write-Error "Input file not found: $InputFile"
    exit 1
}

$lines = Get-Content $InputFile -Encoding utf8

# Parse
$data = @()
foreach ($line in $lines) {
    if ($line -match '^(.*?) \| (.*?) = (.*?) C \| (.*)$') {
        $data += [PSCustomObject]@{
            Hardware = $matches[1].Trim()
            Sensor   = $matches[2].Trim()
            TempRaw  = $matches[3].Trim()
            Temp     = [decimal]($matches[3].Trim())
            Time     = $matches[4].Trim()
        }
    }
}

function Get-TempStatus($temp, $sensorName, $hardwareType) {
    $isDist = $sensorName -like "*Distance to TjMax*"
    if ($isDist) {
        if ($temp -gt 30) { return @{ Css = "temp-normal"; Text = "正常" } }
        elseif ($temp -ge 15) { return @{ Css = "temp-warm"; Text = "略热" } }
        else { return @{ Css = "temp-hot"; Text = "过热" } }
    }
    if ($hardwareType -eq "Cpu") {
        if ($temp -lt 65) { return @{ Css = "temp-normal"; Text = "正常" } }
        elseif ($temp -le 85) { return @{ Css = "temp-warm"; Text = "略热" } }
        else { return @{ Css = "temp-hot"; Text = "过热" } }
    }
    if ($hardwareType -eq "GpuNvidia" -or $hardwareType -eq "GpuAmd") {
        if ($sensorName -like "*Hot Spot*") {
            if ($temp -lt 70) { return @{ Css = "temp-normal"; Text = "正常" } }
            elseif ($temp -le 90) { return @{ Css = "temp-warm"; Text = "略热" } }
            else { return @{ Css = "temp-hot"; Text = "过热" } }
        } else {
            if ($temp -lt 60) { return @{ Css = "temp-normal"; Text = "正常" } }
            elseif ($temp -le 83) { return @{ Css = "temp-warm"; Text = "略热" } }
            else { return @{ Css = "temp-hot"; Text = "过热" } }
        }
    }
    return @{ Css = "temp-normal"; Text = "正常" }
}

# Build HTML rows
$htmlRows = @()
$lastHardware = ""
$rowCount = 0
foreach ($d in $data) {
    $hwEscaped = [System.Net.WebUtility]::HtmlEncode($d.Hardware)
    $sensorEscaped = [System.Net.WebUtility]::HtmlEncode($d.Sensor)
    $st = Get-TempStatus $d.Temp $d.Sensor $d.Hardware
    $groupClass = if ($lastHardware -ne $d.Hardware -and $rowCount -gt 0) { ' class="tr-group"' } else { "" }
    if ($lastHardware -ne $d.Hardware) { $lastHardware = $d.Hardware }
    $htmlRows += "<tr$groupClass><td>$hwEscaped</td><td>$sensorEscaped</td><td class=`"$($st.Css)`">$($d.TempRaw) C</td><td>$($d.Time)</td></tr>"
    $rowCount++
}

# Summary
$cpuPkg = $data | Where-Object { $_.Sensor -eq "CPU Package" } | Select-Object -First 1
$gpuCore = $data | Where-Object { $_.Sensor -eq "GPU Core" } | Select-Object -First 1
$gpuHot = $data | Where-Object { $_.Sensor -eq "GPU Hot Spot" } | Select-Object -First 1

$cpuSt = if ($cpuPkg) { Get-TempStatus $cpuPkg.Temp $cpuPkg.Sensor $cpuPkg.Hardware } else { @{ Css = "temp-normal"; Text = "正常" } }
$gpuCoreSt = if ($gpuCore) { Get-TempStatus $gpuCore.Temp $gpuCore.Sensor $gpuCore.Hardware } else { @{ Css = "temp-normal"; Text = "正常" } }
$gpuHotSt = if ($gpuHot) { Get-TempStatus $gpuHot.Temp $gpuHot.Sensor $gpuHot.Hardware } else { @{ Css = "temp-normal"; Text = "正常" } }

$overallText = "正常"
$overallCss = "temp-normal"
if ($cpuSt.Text -eq "过热" -or $gpuCoreSt.Text -eq "过热" -or $gpuHotSt.Text -eq "过热") {
    $overallText = "过热"
    $overallCss = "temp-hot"
} elseif ($cpuSt.Text -eq "略热" -or $gpuCoreSt.Text -eq "略热" -or $gpuHotSt.Text -eq "略热") {
    $overallText = "略热"
    $overallCss = "temp-warm"
}

$html = @"
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>硬件温度报告</title>
<style>
body { font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif; background: #f5f6fa; padding: 30px; }
.container { max-width: 900px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
h2 { color: #2c3e50; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; margin-bottom: 20px; }
table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #eee; }
th { background: #fafafa; font-weight: 600; color: #555; }
.tr-group td { border-top: 2px solid #ddd; }
.temp-normal { color: #00aa00; font-weight: bold; }
.temp-warm { color: #ff9500; font-weight: bold; }
.temp-hot { color: #ff3333; font-weight: bold; }
.summary-box { background: #f0f7ff; border-left: 4px solid #3498db; padding: 15px 20px; border-radius: 0 8px 8px 0; }
.summary-box h3 { margin: 0 0 10px 0; color: #2c3e50; }
.summary-box p { margin: 6px 0; font-size: 16px; }
.icon { font-size: 20px; margin-right: 6px; vertical-align: middle; }
</style>
</head>
<body>
<div class="container">
<h2>&#x1F4CA; 硬件温度报告（含查询时间）</h2>
<table>
<tr><th>硬件</th><th>项目</th><th>温度</th><th>查询时间</th></tr>
$($htmlRows -join "`n")
</table>
<div class="summary-box">
<h3><span class="icon">&#x1F321;</span>温度总结</h3>
<p><b>CPU Package：</b><span class="$($cpuSt.Css)">$($cpuPkg.TempRaw) C - $($cpuSt.Text)</span></p>
<p><b>GPU Core：</b><span class="$($gpuCoreSt.Css)">$($gpuCore.TempRaw) C - $($gpuCoreSt.Text)</span></p>
<p><b>GPU Hot Spot：</b><span class="$($gpuHotSt.Css)">$($gpuHot.TempRaw) C - $($gpuHotSt.Text)</span></p>
<p><b>整体状态：</b><span class="$overallCss">$overallText</span></p>
</div>
</div>
</body>
</html>
"@

$html | Out-File -FilePath $OutputFile -Encoding utf8 -Force
Start-Process $OutputFile
Write-Output "HTML report generated and opened: $OutputFile"
