---
name: local-password
description: Generate secure random passwords and check password strength. Supports custom length and character types (uppercase, lowercase, numbers, symbols). Pure local operation, no external dependencies. Use when users need to generate new secure passwords or check password strength.
---

# local-password

## Overview

A simple local tool for generating secure random passwords and checking password strength. Fully configurable: choose password length, enable/disable different character types. Estimates password entropy and crack time. All operations run locally, no data leaves your machine.

## Features

- **Generate secure random passwords**: Custom length and character set options
- **Password strength check**: Calculate entropy and estimate crack time
- **Flexible options**: Include/exclude uppercase, lowercase, numbers, symbols
- **Avoid ambiguous characters**: Option to exclude similar looking characters (0O1lI)

## Usage

### Generate password
```bash
# Default: 16 characters, all character types
python3 scripts/generate.py

# Custom length with no symbols
python3 scripts/generate.py --length 20 --no-symbols

# Exclude ambiguous characters
python3 scripts/generate.py --length 12 --no-ambiguous
```

### Check password strength
```bash
python3 scripts/check.py "your-password-here"
```

## Resources

### scripts/
- `generate.py` - Generate secure random password with custom options
- `check.py` - Check password strength and estimate entropy/crack time
