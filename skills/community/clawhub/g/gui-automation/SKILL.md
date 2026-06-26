---
name: desktop-control
description: Control the desktop via CUA computer server API running on port 8000
version: 1.0.0
---

# Desktop Control via CUA Server

This skill allows OpenClaw to control the desktop using the CUA computer server API.

## ⚠️ Security Notice

This skill requires installing and running a third-party server (`cua-computer-sdk`) that has full control over your desktop.

**Before using this skill:**
- The server can simulate keyboard, mouse, and take screenshots
- Only run on systems where you trust all users and processes
- The server runs with your user privileges (no sudo/admin required)
- By default, only accessible from localhost (safe for local use)

## Prerequisites

- Python 3.12+ installed on your system
- CUA computer server running on port 8000 (see installation below)
- Access to localhost:8000 only (network exposure not recommended)

## Installation

### Recommended: Temporary Session (Safest)

Run the server only when needed, in a terminal you can monitor:

```bash
# Install the Computer SDK (official CUA package)
pip install cua-computer-sdk

# Verify package (optional but recommended)
pip show cua-computer-sdk  # Check publisher and version

# Run temporarily (Ctrl+C to stop)
cua-server start --port 8000 --bind 127.0.0.1

# In another terminal, verify it's running locally only
curl http://localhost:8000/status
netstat -an | grep 8000  # Should show 127.0.0.1:8000
```

**This is the safest approach** - the server only runs when you explicitly start it and stops when you close the terminal.

### Alternative: Install from Source

For transparency, you can review and run from source:

```bash
# Clone and review the code first
git clone https://github.com/trycua/cua-computer-server
cd cua-computer-server

# Review the code before running
ls -la
cat requirements.txt  # Check dependencies

# Install and run
pip install -r requirements.txt
python -m cua_server --port 8000 --bind 127.0.0.1
```

### Running the Server

**Option 1: Manual Start (Recommended)**
```bash
# Start in foreground - you can see what it's doing
cua-server start --port 8000

# Stop with Ctrl+C when done
```

**Option 2: Background Process (Temporary)**
```bash
# Run in background for current session only
cua-server start --port 8000 &

# Note the process ID
echo "Server PID: $!"

# Stop when done
kill <PID>
```

**Note:** This skill does NOT require persistent/system service installation. Running the server temporarily when needed is the recommended approach.

## Scope & Limitations

This skill:
- ✅ Controls YOUR desktop when the server is running
- ✅ Runs with YOUR user privileges (no admin/sudo needed)
- ✅ Only accessible from localhost by default

## Security Best Practices

1. **Run Temporarily**: Start the server only when needed, stop when done
2. **Localhost Only**: Keep default binding to 127.0.0.1
3. **No Network Exposure**: Avoid `--bind 0.0.0.0` unless absolutely necessary
4. **Monitor Activity**: Run in foreground to see what commands are executed
5. **Limited Scope**: The server can only do what your user account can do

## Quick Test

After starting the server, verify it works:

```bash
# Simple health check
curl http://localhost:8000/status
# Should return: {"status": "ok"}

# Take a screenshot (safe test)
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "screenshot"}' \
  -o screenshot.json

# If successful, you'll get a JSON response with base64 image data
```

### Troubleshooting

**Port Already in Use:**
```bash
# Check what's using port 8000
lsof -i :8000              # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Solution: Use a different port
cua-server start --port 8001
```

**Permission Denied (Linux):**
```bash
# You may need to add your user to the input group for keyboard/mouse control
sudo usermod -a -G input $USER
# Log out and back in for changes to take effect
```

**Display Not Found (Linux):**
```bash
# Check your display variable
echo $DISPLAY

# Set it explicitly
DISPLAY=:0 cua-server start --port 8000
```

**Server Not Responding:**
```bash
# Check if the process is running
ps aux | grep cua-server       # Linux/macOS
tasklist | findstr cua-server  # Windows

# Try running in foreground to see errors
cua-server start --port 8000 --debug
```

## Available Commands

### Take Screenshot

Capture the current screen:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "screenshot"}' \
  | jq -r '.result.base64' \
  | base64 -d > screenshot.png
```

### Click at Coordinates

Click at specific x,y coordinates:
```bash
# Click at center of 1280x720 screen
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "left_click", "params": {"x": 640, "y": 360}}'
```

### Right Click
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "right_click", "params": {"x": 640, "y": 360}}'
```

### Double Click
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "double_click", "params": {"x": 640, "y": 360}}'
```

### Type Text

Type text at the current cursor position:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "type_text", "params": {"text": "Hello, World!"}}'
```

### Press Hotkey

Press a key combination:
```bash
# Ctrl+C
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "hotkey", "params": {"keys": ["ctrl", "c"]}}'

# Ctrl+Alt+T (open terminal)
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "hotkey", "params": {"keys": ["ctrl", "alt", "t"]}}'
```

### Press Single Key

Press a single key:
```bash
# Press Enter
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "press_key", "params": {"key": "enter"}}'

# Press Escape
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "press_key", "params": {"key": "escape"}}'
```

### Move Cursor

Move cursor to specific position:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "move_cursor", "params": {"x": 100, "y": 200}}'
```

### Scroll

Scroll up or down:
```bash
# Scroll down 3 units
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "scroll_direction", "params": {"direction": "down", "amount": 3}}'

# Scroll up 5 units
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "scroll_direction", "params": {"direction": "up", "amount": 5}}'
```

### Launch Application

Launch an application by name:
```bash
# Launch Firefox
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "launch", "params": {"app": "firefox"}}'

# Launch Terminal
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "launch", "params": {"app": "xfce4-terminal"}}'
```

### Open File or URL

Open a file or URL with default application:
```bash
# Open URL
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "open", "params": {"path": "https://example.com"}}'

# Open file
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "open", "params": {"path": "/home/cua/document.txt"}}'
```

### Get Window Information

Get current window ID:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_current_window_id"}'
```

### Window Control

Maximize window:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "maximize_window", "params": {"window_id": "0x1234567"}}'
```

Minimize window:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "minimize_window", "params": {"window_id": "0x1234567"}}'
```

## Demo Workflows

### Browser Navigation Demo

Open Firefox and navigate to a website:
```bash
# Take initial screenshot
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "screenshot"}' -o initial.json

# Launch Firefox
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "launch", "params": {"app": "firefox"}}'
sleep 3

# Focus address bar (Ctrl+L)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "l"]}}'
sleep 1

# Type URL
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "https://example.com"}}'

# Press Enter
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
sleep 5

# Take final screenshot
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "screenshot"}' -o final.json
```

### Text Editor Demo

Open text editor and type content:
```bash
# Open terminal
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "alt", "t"]}}'
sleep 2

# Type command to open text editor
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "mousepad"}}'
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
sleep 2

# Type some text
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "Hello from OpenClaw!\nThis is automated desktop control."}}'

# Save file (Ctrl+S)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "s"]}}'
sleep 1

# Type filename
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "openclaw-demo.txt"}}'
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
```

### Form Filling Demo

Fill out a web form:
```bash
# Assuming browser is open with form visible

# Click on first input field (adjust coordinates)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "left_click", "params": {"x": 400, "y": 300}}'

# Type name
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "John Doe"}}'

# Tab to next field
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "tab"}}'

# Type email
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "john@example.com"}}'

# Tab to next field
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "tab"}}'

# Type message
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "This form was filled automatically by OpenClaw!"}}'

# Submit form (click submit button)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "left_click", "params": {"x": 400, "y": 500}}'
```

## Helper Functions

### Check Server Status
```bash
curl http://localhost:8000/status
```

### List All Available Commands
```bash
curl http://localhost:8000/commands | jq
```

### Get Screen Size
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_screen_size"}'
```

### Get Cursor Position
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_cursor_position"}'
```

## Environment Variables

- `CUA_SERVER_URL`: Base URL for CUA server (default: http://localhost:8000)

## Tips

1. **Wait Between Commands**: Add `sleep` between commands to allow UI to update
2. **Check Coordinates**: Screen is 1280x720, center is at (640, 360)
3. **Screenshot for Debugging**: Take screenshots before and after actions to verify
4. **Use Variables**: Store coordinates and text in variables for reusability

## Example OpenClaw Usage

Once this skill is loaded, you can use it in OpenClaw conversations:

```
User: "Take a screenshot and open Firefox"
OpenClaw: *executes the screenshot and launch firefox commands*

User: "Type 'Hello World' in the current window"
OpenClaw: *executes the type_text command*

User: "Click at the center of the screen"
OpenClaw: *executes click command at 640,360*
```

## Troubleshooting

1. **Connection Refused**: Make sure CUA server is running on port 8000
2. **No Response**: Check if you're in the container or have SSH tunnel set up
3. **Commands Not Working**: Verify with `curl http://localhost:8000/status`
4. **Wrong Coordinates**: Remember screen is 1280x720, adjust coordinates accordingly