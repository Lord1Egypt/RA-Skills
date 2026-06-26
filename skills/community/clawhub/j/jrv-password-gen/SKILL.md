---
name: password-gen
description: Generate secure passwords, passphrases, and PINs with entropy analysis. Use when the user needs a random password, passphrase, PIN, or wants to check how strong an existing password is. Supports custom length, character sets, exclusions, batch generation, and JSON output. Zero external dependencies.
---

# Password Generator

Generate cryptographically secure passwords, passphrases, and PINs from the command line. Analyze existing passwords for strength. Uses Python `secrets` module for CSPRNG — no external dependencies.

## Quick Start

```bash
# Generate a 16-character password
python3 scripts/password_gen.py

# Generate a 32-character password, 5 at a time
python3 scripts/password_gen.py -l 32 -n 5

# Passphrase (4 random words)
python3 scripts/password_gen.py --passphrase

# 6-word passphrase, capitalized, with number
python3 scripts/password_gen.py --passphrase -w 6 --capitalize --add-number

# PIN
python3 scripts/password_gen.py --pin
python3 scripts/password_gen.py --pin -l 8

# Analyze a password
python3 scripts/password_gen.py --analyze 'MyP@ssw0rd!'

# JSON output
python3 scripts/password_gen.py --json
```

## Commands

| Flag | Description |
|------|-------------|
| `-l, --length N` | Password length (default: 16) |
| `-n, --count N` | Generate N passwords |
| `--no-uppercase` | Exclude uppercase letters |
| `--no-lowercase` | Exclude lowercase letters |
| `--no-digits` | Exclude digits |
| `--no-symbols` | Exclude symbols |
| `--exclude CHARS` | Exclude ambiguous chars like `lI1O0` |
| `--must-include CHARS` | Force specific characters to appear |
| `--passphrase` | Word-based passphrase mode |
| `-w, --words N` | Words in passphrase (default: 4) |
| `--separator SEP` | Passphrase separator (default: `-`) |
| `--capitalize` | Capitalize passphrase words |
| `--add-number` | Append random number to passphrase |
| `--pin` | Numeric PIN mode |
| `--analyze PW` | Analyze existing password strength |
| `--json` | JSON output |

## Entropy Guide

| Bits | Strength | Use Case |
|------|----------|----------|
| < 28 | Very Weak | Never use |
| 28-35 | Weak | Throwaway accounts only |
| 36-59 | Moderate | General accounts |
| 60-79 | Strong | Important accounts |
| 80-127 | Very Strong | Financial, admin |
| 128+ | Excellent | Master passwords, encryption keys |
