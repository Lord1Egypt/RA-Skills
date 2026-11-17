---
name: pc-temp-monitor
description: Query CPU and GPU temperatures on Windows PCs using LibreHardwareMonitor, generate a colored HTML report opened in browser, and output a text summary with timestamp. Use when the user asks about PC temperature, CPU temperature, GPU temperature, hardware temperature monitoring, or thermal status on Windows.
---

# PC Temperature Monitor

Query hardware temperature sensors on Windows and present results in both a colored HTML report and a text table.

## Prerequisites

- Windows OS
- PowerShell 5.1 or later
- Administrator privileges are required to read CPU temperature sensors

## LibreHardwareMonitor Setup

1. Check if `LibreHardwareMonitor` exists at `$env:TEMP\LibreHardwareMonitor\LibreHardwareMonitorLib.dll`.
2. If missing, download the latest release zip from `https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/latest`.
   - Look for the asset named `LibreHardwareMonitor.zip`.
   - Download it to `$env:TEMP\LibreHardwareMonitor.zip`.
   - Extract it to `$env:TEMP\LibreHardwareMonitor\`.
3. Verify `LibreHardwareMonitorLib.dll` exists after extraction.

## Query Workflow

### 1. Elevated Temperature Query

Use `scripts/query-temp.ps1` to perform the actual sensor reading. Because CPU temperature sensors require admin rights, launch it via `Start-Process -Verb RunAs`.

Example:
```powershell
$queryScript = "$env:TEMP\lhm_query.ps1"
# Copy or reference scripts/query-temp.ps1 content
Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$queryScript`"" -ErrorAction Stop
```

Wait up to 20 seconds for the output file `$env:TEMP\lhm_temps_result.txt` to appear.

### 2. Read Results

Parse the result file. Each line format:
```
<Hardware Name> | <Sensor Name> = <Value> C | <yyyy/M/d HH:mm:ss>
```

### 3. Generate HTML Report

Use `scripts/generate-html.ps1` to produce the colored HTML report and open it in the default browser.

Example:
```powershell
& "<skill-dir>\scripts\generate-html.ps1" -InputFile "$env:TEMP\lhm_temps_result.txt"
```

The script automatically classifies temperatures and applies colors:
- **Green** (`temp-normal`): Normal range
- **Orange** (`temp-warm`): Warm / slightly hot
- **Red** (`temp-hot`): Overheating

Classification rules:
- **CPU** (`Cpu`): `< 65 C` normal, `65-85 C` warm, `> 85 C` hot
- **GPU Core** (`GpuNvidia`/`GpuAmd`): `< 60 C` normal, `60-83 C` warm, `> 83 C` hot
- **GPU Hot Spot**: `< 70 C` normal, `70-90 C` warm, `> 90 C` hot
- **Distance to TjMax**: `> 30` normal, `15-30` warm, `< 15` hot

### 4. Text Summary Output

After opening the HTML report, output a Markdown text summary in the chat with this exact structure:

1. **Main table** with columns: `Hardware`, `Sensor`, `Temperature`, `Query Time`
2. **Summary table** with columns: `Hardware`, `Key Metric`, `Temperature`
3. **Status lines** prefixed with `🌡️ 温度总结:`
   - `CPU: <正常/略热/过热>`
   - `GPU: <正常/略热/过热>`
   - `Overall: <正常/略热/过热>`

Keep the summary concise. Do not add suggestions or lengthy explanations unless explicitly requested.

## Notes

- If the user says `temp` as a standalone command, execute the full workflow immediately.
- The HTML report is saved to `$env:TEMP\temperature_report.html` and overwritten on each run.
- UAC behavior depends on local Windows policy. If `ConsentPromptBehaviorAdmin` is `0` for admin users, elevation may be silent. Otherwise the user may see a UAC prompt.
