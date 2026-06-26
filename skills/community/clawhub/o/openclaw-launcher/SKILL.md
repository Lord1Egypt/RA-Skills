---
name: openclaw-launcher
description: |
  Create Windows desktop shortcut and scripts for one-click OpenClaw startup on WSL.
  Use when: (1) user asks to create/open/fix OpenClaw launcher, (2) user reports
  "gateway disconnected" or "gateway stopping" errors, (3) shortcut icon not showing,
  (4) batch/PowerShell script errors. Handles: WSL portproxy setup, systemd service
  check/start, keep-alive process, Windows shortcut with .ico icon, hidden window mode.
---

# OpenClaw Launcher

## Prerequisites

One-click startup for OpenClaw Gateway via Windows desktop shortcut.

## Prerequisites

- WSL2 with Ubuntu (or other distro)
- OpenClaw Gateway installed in WSL as systemd user service
- Windows PowerShell or PowerShell 7
- Python with PIL/Pillow (for icon conversion)

## Architecture

```
Desktop Shortcut (.lnk)
    ↓
<USER_SCRIPTS_DIR>\start-openclaw.bat
    ↓
start-openclaw.ps1 (hidden, auto-close)
    ↓
WSL: systemctl start openclaw-gateway + keep-alive sleep
    ↓
Dashboard opens in browser
```

## Path Reference

**Important:** WSL and Windows paths are different:

| System | Path Example |
|--------|--------------|
| Windows | `C:\Users\<WINDOWS_USER>\openclaw-scripts\` |
| WSL | `/mnt/c/Users/<WINDOWS_USER>/openclaw-scripts/` |
| WSL home | `/home/<WSL_USER>/` |

When working in WSL, use `/mnt/c/...` prefix to access Windows files.
When working in PowerShell on Windows, use `C:\...` paths.

**Note on scripts/ directory:** The `scripts/` folder contains reference templates. When deploying, these are copied to `C:\Users\<WINDOWS_USER>\openclaw-scripts\` with actual usernames substituted. Always use the Python method to generate scripts on the user's machine (see Step 3).

## Step-by-Step Workflow

### Step 1: Gather System Info

**Auto-detect Windows username:**
```powershell
$WindowsUser = $env:USERNAME
Write-Host "Windows user: $WindowsUser"
```

**Get WSL distro name (in Windows CMD or PowerShell):**
```cmd
wsl --list
```

**Get WSL username (in WSL terminal):**
```bash
whoami
```

**Default shortcut name:** Ask user or use "OpenClaw"

### Step 2: Create Scripts Directory

In Windows PowerShell (as user, no admin needed):
```powershell
New-Item -ItemType Directory -Path "C:\Users\<WINDOWS_USER>\openclaw-scripts" -Force
```
Replace `<WINDOWS_USER>` with actual Windows username, or use `$env:USERNAME`.

Or from WSL:
```bash
mkdir -p /mnt/c/Users/<WINDOWS_USER>/openclaw-scripts
```

### Step 3: Write Core Script (start-openclaw.ps1)

**⚠️ Important: Always write .ps1 files using Python (not bash heredocs) to avoid escaping issues.**

**Key variables to customize:**
- `$WslDistro`: WSL distro name (e.g., "Ubuntu")
- `$WslUser`: WSL username (from `whoami`)

**Step 3a: Write keep-alive.bat first (required for reliable backgrounding)**

```python
content = '@echo off\nstart "" /b cmd /c wsl.exe --distribution Ubuntu --user <WSL_USER> -- bash -c "sleep 86400"\n'
with open('/mnt/c/Users/<WINDOWS_USER>/openclaw-scripts/keep-alive.bat', 'w', encoding='ascii') as f:
    f.write(content)
```

**Step 3b: Write start-openclaw.ps1 using Python**

```python
lines = [
    '# OpenClaw Gateway Launcher Script (Hidden Mode)',
    '',
    '$wslConfig = cmd /c "wsl.exe --distribution Ubuntu --user <WSL_USER> -- cat ~/.openclaw/openclaw.json 2>&1"',
    '$tokenMatch = [regex]::Match($wslConfig, "[a-f0-9]{40}")',
    'if ($tokenMatch.Success) {',
    '    $TOKEN = $tokenMatch.Value',
    '} else {',
    '    Write-Host "[ERROR] Failed to read token from WSL config"',
    '    exit 1',
    '}',
    '$DASHBOARD_URL = "http://localhost:18789/#token=$TOKEN"',
    '',
    '# Get WSL IP',
    '$wslIpRaw = cmd /c "wsl.exe --distribution Ubuntu --user <WSL_USER> -- hostname -I 2>&1"',
    '$wslIp = ($wslIpRaw -split " ")[0]',
    '',
    '# Setup port proxy (requires admin)',
    'cmd /c "netsh interface portproxy delete v4tov4 listenport=18789 listenaddress=127.0.0.1 2>nul"',
    'cmd /c "netsh interface portproxy add v4tov4 listenport=18789 listenaddress=127.0.0.1 connectport=18789 connectaddress=$wslIp protocol=tcp 2>nul"',
    '',
    '# Check and start service if needed',
    '$status = cmd /c "wsl.exe --distribution Ubuntu --user <WSL_USER> -- systemctl --user is-active openclaw-gateway 2>&1"',
    'if ($status -ne "active") {',
    '    cmd /c "wsl.exe --distribution Ubuntu --user <WSL_USER> -- systemctl --user start openclaw-gateway 2>nul"',
    '    Start-Sleep -Seconds 3',
    '}',
    '',
    '# Start keep-alive via pre-created batch file (more reliable than inline Start-Process)',
    'Start-Process -FilePath "cmd.exe" -ArgumentList "/c","C:\\Users\\<WINDOWS_USER>\\openclaw-scripts\\keep-alive.bat" -WindowStyle Hidden',
    '',
    '# Open Dashboard',
    'start $DASHBOARD_URL',
]

content = '\n'.join(lines)
with open('/mnt/c/Users/<WINDOWS_USER>/openclaw-scripts/start-openclaw.ps1', 'wb') as f:
    f.write(b'\xef\xbb\xbf')  # UTF-8 BOM for PowerShell
    f.write(content.encode('utf-8'))
```

### Step 4: Write Bat Launcher

```powershell
$batContent = '@echo off
chcp 65001 >nul
powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0start-openclaw.ps1"'

Set-Content -Path "C:\Users\<WINDOWS_USER>\openclaw-scripts\start-openclaw.bat" -Value $batContent -Encoding ASCII
```

**Note**: The .bat must use `-ExecutionPolicy Bypass` to allow the script to run without prompts.

### Step 5: Prepare Icon (Optional)

1. Get PNG image (256x256 or larger)
2. Copy to Windows scripts folder or accessible location
3. Convert to ICO using Python in WSL:

```bash
# If PNG is at Windows path (accessible from WSL):
python3 -c "
from PIL import Image
img = Image.open('/mnt/c/Users/<WINDOWS_USER>/Desktop/icon.png')
img = img.resize((256, 256), Image.Resampling.LANCZOS)
img.save('/mnt/c/Users/<WINDOWS_USER>/openclaw-scripts/icon.ico', format='ICO')
"
```

### Step 6: Create Desktop Shortcut

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\<WINDOWS_USER>\Desktop\<SHORTCUT_NAME>.lnk")
$Shortcut.TargetPath = "C:\Users\<WINDOWS_USER>\openclaw-scripts\start-openclaw.bat"
$Shortcut.WorkingDirectory = "C:\Users\<WINDOWS_USER>\openclaw-scripts"
$Shortcut.IconLocation = "C:\Users\<WINDOWS_USER>\openclaw-scripts\icon.ico"
$Shortcut.Save()
```

### Step 7: Test

1. Double-click shortcut
2. Verify: No visible PowerShell window
3. Verify: Browser opens dashboard URL
4. Verify: Gateway is active:
   ```bash
   systemctl --user is-active openclaw-gateway
   ```
5. Verify: Keep-alive process running (in WSL):
   ```bash
   ps aux | grep "sleep 86400"
   ```
   Should show a `sleep 86400` process owned by your user.

### Step 8: Verify No "Gateway Stopping" Issues

If gateway stops immediately after script runs, check:
1. Is keep-alive process running? (`ps aux | grep sleep`)
2. If not, the batch file path in `Start-Process` may be wrong
3. Try running the script with admin privileges for portproxy

## Troubleshooting

### "Gateway disconnected" / "Gateway stopping" immediately
**Cause**: Keep-alive process dies when PowerShell exits
**Fix**: Use a pre-created batch file for keep-alive, not inline `Start-Process`. See Step 3 script template.

### Keep-alive process not running after script exits
**Cause**: `Start-Process -WindowStyle Hidden` creates a process that dies when PowerShell exits
**Fix**: The keep-alive must be a separate .bat file started via `cmd /c`:
```powershell
# In start-openclaw.ps1:
Start-Process -FilePath "cmd.exe" -ArgumentList "/c","C:\Users\<WINDOWS_USER>\openclaw-scripts\keep-alive.bat" -WindowStyle Hidden
```
And pre-create `keep-alive.bat`:
```bat
@echo off
start "" /b cmd /c wsl.exe --distribution Ubuntu --user <WSL_USER> -- bash -c "sleep 86400"
```

### Token extraction fails / $Matches is empty
**Cause**: Two issues:
1. Regex matches "mode": "token" before actual token field
2. `$Matches` doesn't populate correctly after `cmd /c` calls
**Fix**: Use `[regex]::Match()` with 40-char hex pattern:
```powershell
$wslConfig = cmd /c "wsl.exe --distribution Ubuntu --user <WSL_USER> -- cat ~/.openclaw/openclaw.json 2>&1"
$tokenMatch = [regex]::Match($wslConfig, "[a-f0-9]{40}")
if ($tokenMatch.Success) {
    $TOKEN = $tokenMatch.Value
}
```

### PowerShell script parsing errors after editing
**Cause**: Bash/WSL heredoc escaping corrupts PowerShell syntax (especially backticks `\s`, `$`, etc.)
**Fix**: Write PowerShell files using Python, not bash heredocs:
```python
content = '''# PowerShell content here
$var = "value"
'''
with open('/mnt/c/Users/.../script.ps1', 'wb') as f:
    f.write(b'\xef\xbb\xbf')  # UTF-8 BOM
    f.write(content.encode('utf-8'))
```

### PowerShell shows "unexpected token" errors
**Cause**: File encoding issues or special characters not handled
**Fix**: Always write PowerShell scripts with UTF-8 BOM encoding (`-Encoding UTF8` in PowerShell, or `b'\xef\xbb\xbf'` in Python)

### "Script moved or changed" when clicking shortcut
**Cause**: Shortcut points to WSL UNC path (`\\wsl$\...`)
**Fix**: Scripts must be in Windows-native path (`C:\Users\...\openclaw-scripts\`)

### Icon not displaying correctly
**Cause**: Shortcut references .png instead of .ico, or wrong path
**Fix**: Convert PNG to ICO, verify IconLocation path exists

### Portproxy connection refused
**Cause**: Gateway only listens on 127.0.0.1, or portproxy not set up
**Fix**: 
1. Run script as Administrator (portproxy requires admin)
2. Or manually verify:
```cmd
netsh interface portproxy show all
```

### WSL commands fail silently
**Cause**: PowerShell `&` operator doesn't handle spaces well
**Fix**: Always use `cmd /c "wsl.exe ..."` pattern

### WSL distro not found
**Cause**: Distro name spelling is wrong
**Fix**: List all distros:
```cmd
wsl --list --verbose
```

### Debugging script issues from WSL
When troubleshooting PowerShell scripts, run directly via:
```bash
/mnt/c/Windows/System32/cmd.exe /c "cd /d C:\\Users\\<WINDOWS_USER>\\openclaw-scripts && powershell -ExecutionPolicy Bypass -File start-openclaw.ps1"
```

## Security Notes

- Token is read dynamically from WSL config at runtime
- Never hardcode tokens or credentials
- Keep scripts in user-private directory
- Portproxy only exposes local loopback
