---
name: otpforge
description: Manage TOTP/2FA codes locally (add/list/remove accounts, display current codes, and optional Tkinter GUI). Use when a user asks to generate a TOTP code, store a new base32 secret, list 2FA accounts, or manage a local OTP vault from the command line.
---

# OtpForge

Use the bundled `cli.py` and `core.py` to manage a local JSON vault of TOTP secrets and to generate current codes.

## Quickstart (CLI)

- List accounts:
  - `python3 cli.py list`
  - `python3 cli.py list --codes`
- Add/update an account:
  - `python3 cli.py add <label> <base32-secret> --issuer <issuer> --digits 6 --period 30`
- Get one code:
  - `python3 cli.py code <label>`
- Remove:
  - `python3 cli.py remove <label>`

## Vault location

- Default: `~/.config/otpforge/secrets.json`
- Override with env var: `OTPFORGE_STORE=/path/to/secrets.json`
- Override with CLI flag (preferred for one-offs): `python3 cli.py --store /path/to/secrets.json ...`

## GUI

- Launch: `python3 cli.py gui`

Notes:
- The GUI is a simple Tkinter app that refreshes codes every second.
- Secrets are masked in the input field.
