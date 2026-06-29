# Linux System Controller - Command Reference

## Script Locations

All scripts are located at: `scripts/`

---

## 1. window_manager.py - Window Management

### List all visible windows
```bash
python3 scripts/window_manager.py list
```
Returns JSON array of windows with window_id, title, pid, and desktop.

### Activate (bring to foreground)
```bash
python3 scripts/window_manager.py activate --title "Terminal"
python3 scripts/window_manager.py activate --window-id 0x1400001
python3 scripts/window_manager.py activate --pid 1234
```

### Close a window
```bash
python3 scripts/window_manager.py close --title "Untitled - Terminal"
python3 scripts/window_manager.py close --window-id 0x1400001
```

### Minimize / Maximize
```bash
python3 scripts/window_manager.py minimize --title "Terminal"
python3 scripts/window_manager.py maximize --window-id 0x1400001
```

### Resize and move
```bash
python3 scripts/window_manager.py resize --window-id 0x1400001 --x 100 --y 100 --width 800 --height 600
```

### Move a window
```bash
python3 scripts/window_manager.py move --title "Terminal" --x 200 --y 200
```

### Send keystrokes to window
```bash
python3 scripts/window_manager.py send-keys --title "Terminal" --text "Hello World"
```

---

## 2. process_manager.py - Process Management

### List all processes (top 20 by CPU)
```bash
python3 scripts/process_manager.py list
```

### List processes by name
```bash
python3 scripts/process_manager.py list --name chrome
```

### Kill a process
```bash
python3 scripts/process_manager.py kill --pid 1234
python3 scripts/process_manager.py kill --name firefox
```

### Start a process
```bash
python3 scripts/process_manager.py start "gedit"
python3 scripts/process_manager.py start "firefox"
```

### Get process info
```bash
python3 scripts/process_manager.py info --pid 1234
```

### Get system information
```bash
python3 scripts/process_manager.py system
```

---

## 3. hardware_controller.py - Hardware Control

### Volume control

#### Get current volume
```bash
python3 scripts/hardware_controller.py volume get
```

#### Set volume (0-100)
```bash
python3 scripts/hardware_controller.py volume set --level 50
```

#### Mute/Unmute
```bash
python3 scripts/hardware_controller.py volume mute
python3 scripts/hardware_controller.py volume unmute
```

### Screen brightness

#### Get brightness
```bash
python3 scripts/hardware_controller.py screen brightness get
```

#### Set brightness (0-100)
```bash
python3 scripts/hardware_controller.py screen brightness set --level 70
```

### Power management

#### Lock screen
```bash
python3 scripts/hardware_controller.py power lock
```

#### Sleep (suspend)
```bash
python3 scripts/hardware_controller.py power sleep
```

#### Hibernate
```bash
python3 scripts/hardware_controller.py power hibernate
```

#### Shutdown
```bash
python3 scripts/hardware_controller.py power shutdown
```

#### Restart
```bash
python3 scripts/hardware_controller.py power restart
```

### Network

#### List network adapters
```bash
python3 scripts/hardware_controller.py network list
```

#### Enable adapter
```bash
python3 scripts/hardware_controller.py network enable --adapter eth0
```

#### Disable adapter
```bash
python3 scripts/hardware_controller.py network disable --adapter eth0
```

#### Scan WiFi networks
```bash
python3 scripts/hardware_controller.py network wifi
```

#### Get network info
```bash
python3 scripts/hardware_controller.py network info
```

### USB

#### List USB devices
```bash
python3 scripts/hardware_controller.py usb list
```

---

## 4. serial_comm.py - Serial Communication

### List available serial ports
```bash
python3 scripts/serial_comm.py list
```
Returns JSON array of available serial ports.

### Send data to port
```bash
python3 scripts/serial_comm.py send --port /dev/ttyUSB0 --data "LED_ON"
```

### Receive data from port
```bash
python3 scripts/serial_comm.py receive --port /dev/ttyUSB0 --timeout 5
```

### Chat mode (send and receive)
```bash
python3 scripts/serial_comm.py chat --port /dev/ttyUSB0 --data "GET_TEMP"
```

### Monitor port continuously
```bash
python3 scripts/serial_comm.py monitor --port /dev/ttyUSB0 --duration 30
```

---

## 5. iot_controller.py - IoT Controller

### Home Assistant

#### List all entities
```bash
python3 scripts/iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN list
```

#### Get entity state
```bash
python3 scripts/iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN state --entity-id light.living_room
```

#### Turn on device
```bash
python3 scripts/iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN on --entity-id light.living_room
```

#### Turn off device
```bash
python3 scripts/iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN off --entity-id light.bedroom
```

#### Toggle device
```bash
python3 scripts/iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN toggle --entity-id switch.kitchen
```

#### Call custom service
```bash
python3 scripts/iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN call_service --domain light --service turn_on --service_data '{"brightness": 255}'
```

### Generic HTTP

#### GET request
```bash
python3 scripts/iot_controller.py http --url http://192.168.1.50/api get --path /status
```

#### POST request
```bash
python3 scripts/iot_controller.py http --url http://192.168.1.50/api post --path /command --body '{"command":"on"}'
```

#### PUT request
```bash
python3 scripts/iot_controller.py http --url http://192.168.1.50/api put --path /config --body '{"mode":"auto"}'
```

#### With custom headers
```bash
python3 scripts/iot_controller.py http --url http://192.168.1.50/api get --path /data --headers '{"Authorization":"Bearer token123"}'
```

---

## 6. gui_controller.py - GUI Control

### Mouse

#### Get mouse position
```bash
python3 scripts/gui_controller.py mouse position
```

#### Move mouse
```bash
python3 scripts/gui_controller.py mouse move --x 500 --y 300
```

#### Click
```bash
python3 scripts/gui_controller.py mouse click --x 500 --y 300
python3 scripts/gui_controller.py mouse click  # Click at current position
```

#### Right click
```bash
python3 scripts/gui_controller.py mouse right-click --x 500 --y 300
```

#### Double click
```bash
python3 scripts/gui_controller.py mouse double-click --x 500 --y 300
```

#### Drag
```bash
python3 scripts/gui_controller.py mouse drag --start-x 100 --start-y 200 --end-x 500 --end-y 400
```

#### Scroll
```bash
python3 scripts/gui_controller.py mouse scroll --direction down --clicks 10
python3 scripts/gui_controller.py mouse scroll --direction up --clicks 5
```

### Keyboard

#### Type text
```bash
python3 scripts/gui_controller.py keyboard type --text "Hello World"
```

#### Press hotkeys
```bash
python3 scripts/gui_controller.py keyboard press --keys "ctrl+c"
python3 scripts/gui_controller.py keyboard press --keys "alt+tab"
python3 scripts/gui_controller.py keyboard press --keys "ctrl+shift+t"
```

### Screenshot

#### Full screen
```bash
python3 scripts/gui_controller.py screenshot full
```

#### Region
```bash
python3 scripts/gui_controller.py screenshot region --x 100 --y 100 --width 800 --height 600
```

#### Get screen size
```bash
python3 scripts/gui_controller.py screenshot size
```

### Visual (OCR and Image Recognition)

#### OCR full screen
```bash
python3 scripts/gui_controller.py visual ocr
```

#### OCR region
```bash
python3 scripts/gui_controller.py visual ocr --x 100 --y 100 --width 800 --height 600
```

#### Find template on screen
```bash
python3 scripts/gui_controller.py visual find --template button.png
```

#### Click image template
```bash
python3 scripts/gui_controller.py visual click-image --template submit.png
```

#### Get pixel color
```bash
python3 scripts/gui_controller.py visual pixel --x 200 --y 200
```

---

## Notes

- All commands return JSON output for easy parsing
- Use `python3` to run scripts (Python 3.6+ required)
- Some commands require additional system tools:
  - `xdotool`, `wmctrl` for window management
  - `amixer`, `xbacklight` for hardware control
  - `tesseract-ocr` for OCR functionality
- Install system tools with: `apt-get install xdotool wmctrl tesseract-ocr alsa-utils`
- Python dependencies are auto-installed on first use
