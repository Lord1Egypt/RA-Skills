---
name: mac-clamshell-mode
description: Mac laptop clamshell mode assistant. Supports running with lid closed WITHOUT external display/keyboard/mouse. Auto-detects Mac model and macOS version, provides safe configuration with rollback.
---

# Mac Clamshell Mode Assistant

## Overview

Helps Mac users configure their laptops to run tasks with the lid closed. **No external display, keyboard, or mouse required!** This skill detects the current Mac model and macOS version, then provides appropriate configuration steps.

## Key Features

- ✅ **No external display required** - Works with laptop alone
- ✅ **No external keyboard/mouse required** - Pure headless operation
- ✅ **Auto-detection** - Identifies Mac model and macOS version
- ✅ **Multiple modes** - Standard clamshell, forced headless, or temporary
- ✅ **Safe configuration** - Requires explicit approval, includes rollback
- ✅ **Battery warnings** - Alerts about power consumption

## When to use

- User wants to run background tasks with MacBook lid closed
- User needs headless operation without external peripherals
- User wants to verify current power management settings
- User needs help with Amphetamine or caffeinate commands
- User wants to restore default power settings

## System Requirements

- macOS 10.15 Catalina or later
- MacBook (Pro/Air) - Intel or Apple Silicon
- Power adapter connected (strongly recommended for headless mode)

## Configuration Modes

### Mode 1: Standard Clamshell (Requires External Display)
- Traditional macOS clamshell mode
- Most stable, most power-efficient
- Requires: Power + External Display + Keyboard/Mouse

### Mode 2: Forced Headless Operation ⭐ RECOMMENDED
- **No external display required**
- **No external keyboard/mouse required**
- Modifies system power settings
- Perfect for background tasks, servers, rendering
- Warning: Increased battery consumption

### Mode 3: Temporary Operation
- Uses `caffeinate` command
- No system setting changes
- Good for short-term tasks
- Stops when terminal closes

### Mode 4: Status Check
- View current power settings
- See what's preventing sleep
- No modifications

### Mode 5: Restore Defaults
- Rollback all changes
- Return to factory power settings

## Workflow

### 1) System Detection
- Mac model (MacBook Pro/Air identification)
- macOS version (10.15+ compatibility check)
- Current power management settings
- Amphetamine running status

### 2) User Selection
- Present 5 configuration modes
- Clear explanations for each option
- Explicit confirmation required

### 3) Apply Configuration
- Mode-specific setup
- Safety warnings displayed
- Success/failure feedback

### 4) Verification & Rollback
- Test current sleep prevention status
- Provide rollback instructions
- Include recovery commands

## Safety Rules

- ⚠️ **Always recommend power adapter** for headless mode
- ⚠️ **Warn about battery drain** when running without external display
- ✅ **Require explicit approval** before making system changes
- ✅ **Provide rollback instructions** for all configurations
- ✅ **Check Amphetamine status** and recommend if not running