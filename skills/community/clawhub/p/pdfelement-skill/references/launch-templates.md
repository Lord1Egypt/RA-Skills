# PDFelement Launch Templates

Use these copy-ready templates when launching PDFelement workflows with a preloaded PDF.

## Windows (wspet:// Protocol - Required)

**Important:** Windows requires PDFelement 12.1.14+ with `wspet://` protocol registered.
**Every Windows command must include `-wsclaw -autoexec -entrance OpenClaw`.**
Prefer the bundled PowerShell helper because it builds the file payload without requiring Python.

### Recommended helper

```powershell
.\scripts\launch_wspet.ps1 -Command convert -TargetFormat .docx -Files @("C:\Docs\input.pdf")
.\scripts\launch_wspet.ps1 -Command optimize -Files @("C:\Docs\large.pdf")
.\scripts\launch_wspet.ps1 -Command watermark -Files @("C:\Docs\document.pdf")
```

### Convert PDF to Word

```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\input.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$filePayload = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "convert -t .docx -f $filePayload -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

### Convert PDF to Excel

```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\input.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$filePayload = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "convert -t .xlsx -f $filePayload -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

### Convert PDF to PowerPoint

```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\input.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$filePayload = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "convert -t .pptx -f $filePayload -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

### Convert PDF to Text

```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\input.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$filePayload = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "convert -t .txt -f $filePayload -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

### OCR PDF

```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\scanned.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$filePayload = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "ocr -f $filePayload -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

### Optimize/Compress PDF

```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\large.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$filePayload = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "optimize -f $filePayload -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

### Translate PDF

```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\document.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$filePayload = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "translate -f $filePayload -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

### Using Python helper script (optional)

```powershell
python scripts\launch_wspet.py convert --format .docx --files "C:\Docs\input.pdf"
python scripts\launch_wspet.py ocr --files "C:\Docs\scanned.pdf"
python scripts\launch_wspet.py optimize --files "C:\Docs\large.pdf"
```

### Protocol Failure Handling

```powershell
# Normal task launches should skip empty probes and send the real wspet://param=... command directly.
# If Start-Process fails with an association error, tell the user to install/update PDFelement.
```

If this fails with "No application is associated with the specified file", PDFelement is not installed or the version is too old.

### If Protocol Is Not Available

**Download and install PDFelement:**
1. Download from: **https://pdf.wondershare.com/**
2. Install version 12.1.14 or later
3. Restart system to register the `wspet://` protocol
4. Verify with the launch test above

### Notes

- **Always use `wspet://` protocol on Windows**; direct `PDFToolbox.exe` execution is deprecated.
- Prefer `scripts\launch_wspet.ps1` on Windows because it does not require Python.
- If `scripts\launch_wspet.ps1` is missing but `scripts\launch_wspet.ps1.md` exists, copy the `.md` file to `scripts\launch_wspet.ps1` before launching PDFelement.
- Replace `C:\Docs\input.pdf` with actual absolute paths.
- The `-wsclaw -autoexec -entrance OpenClaw` flags are mandatory for all Windows commands.
- The GUI opens with files pre-loaded; user can cancel during the countdown.
- Output files are created beside the source PDF unless GUI settings specify otherwise.
- Run from the logged-in desktop session for GUI access.

## Ubuntu/Linux

### Convert PDF to Word

```bash
cd /opt/apps/PDFelement && ./PDFToolbox convert -t ".docx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

### Convert PDF to PowerPoint

```bash
cd /opt/apps/PDFelement && ./PDFToolbox convert -t ".pptx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

### Convert PDF to Text

```bash
cd /opt/apps/PDFelement && ./PDFToolbox convert -t ".txt" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

### Convert PDF to Excel

```bash
cd /opt/apps/PDFelement && ./PDFToolbox convert -t ".xlsx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

### Agent/Desktop Session Template

```bash
cd /opt/apps/PDFelement && DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ./PDFToolbox convert -t ".docx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

### If Changing Directory Is Inconvenient

```bash
LD_LIBRARY_PATH=/opt/apps/PDFelement /opt/apps/PDFelement/PDFToolbox convert -t ".docx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

### Notes

- Use absolute file paths only.
- Prefer running from the active desktop session when GUI launch is required.
- Reuse `DISPLAY`, `XAUTHORITY`, and `DBUS_SESSION_BUS_ADDRESS` when an agent or service must open the GUI.
- On this machine, `.docx`, `.pptx`, and `.txt` have already been verified with the preloaded-file flow.
