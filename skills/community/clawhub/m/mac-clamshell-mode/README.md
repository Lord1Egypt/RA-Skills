# Mac Clamshell Mode Assistant

## Overview

A comprehensive tool to enable and manage clamshell mode (closed-lid operation) on macOS devices. This skill automatically detects your Mac model and macOS version, then provides the optimal configuration for your specific setup.

## Features

- ✅ **Automatic Detection**: Identifies Mac model and macOS version
- ✅ **Compatibility Check**: Verifies if your system supports clamshell mode
- ✅ **One-click Configuration**: Sets up optimal power management settings
- ✅ **Amphetamine Integration**: Configures Amphetamine for seamless operation
- ✅ **Safety First**: Includes rollback options and safety checks
- ✅ **Multi-version Support**: Works across different macOS versions (10.15+)

## System Requirements

- macOS 10.15 Catalina or later
- External power adapter (required for clamshell mode)
- External display, keyboard, and mouse (recommended for full clamshell mode)
- Administrator privileges for system configuration

## Usage

### Basic Usage
```bash
# Check compatibility
./check-compatibility.sh

# Configure clamshell mode
./configure-clamshell.sh
```

### Advanced Options
```bash
# Configure with specific settings
./configure-clamshell.sh --power-only    # Only configure power settings
./configure-clamshell.sh --amphetamine   # Only configure Amphetamine
./configure-clamshell.sh --rollback      # Restore original settings
```

## Safety Notes

- Always connect to external power before enabling clamshell mode
- The script creates backup files of your original settings
- Use `--rollback` option to restore original configuration
- Test thoroughly before relying on this for critical workloads

## Supported Mac Models

- MacBook Air (2018 and later)
- MacBook Pro (2016 and later)
- Mac mini (2018 and later)
- iMac (2019 and later)
- Mac Studio (all models)
- Mac Pro (2019 and later)

## Troubleshooting

### Common Issues

1. **System still sleeps when lid is closed**
   - Ensure external power is connected
   - Verify Amphetamine is running and active
   - Check that external display is properly connected

2. **Settings not persisting after reboot**
   - Run the script again after system updates
   - Some macOS updates reset power management settings

3. **Amphetamine not preventing sleep**
   - Ensure Amphetamine has proper permissions in System Preferences
   - Check that "Prevent sleep" is enabled in Amphetamine settings

### Debugging Commands

```bash
# Check current power settings
pmset -g

# Check what's preventing sleep
pmset -g assertions

# View system logs for sleep events
log show --predicate 'eventMessage contains "Sleep"' --last 1h
```

## License

This skill is provided under the MIT License. See LICENSE file for details.

## Author

Created by OpenClaw Assistant for the ClawHub community.