# nfc-tools skill

## Overview
`nfc-tools` documents how to discover NFC readers, inspect tags, and perform cautious reads/writes with the `libnfc`/`nfc-utils` stack. It keeps safety front-and-center by requiring explicit confirmation before every destructive write and by providing an offline fallback when the NFC hardware is not present.

## Requirements
- `libnfc` and the associated command-line utilities (`nfc-list`, `nfc-poll`, `nfc-taginfo`, `nfc-mfultralight`, `nfc-mfclassic`).
- A compatible NFC reader (PN532, ACR122U, SCL3711, etc.) supported by your OS driver.
- On Linux, udev rules under `/etc/udev/rules.d/` (copy from `contrib/udev/93-pn53x.rules` if needed).
- If you use macOS, install `libusb`/`libnfc` via Homebrew before installing the utilities.

## Installation
### macOS (Homebrew)
```sh
brew install libnfc libfreefare
brew install nfcutils  # if available in the tap, otherwise build libnfc examples
```

### Debian/Ubuntu
```sh
sudo apt update
sudo apt install libnfc-bin libnfc-utils libnfc-examples
```

After installing, copy the sample configuration and rules if you have physical readers:
```sh
sudo mkdir -p /etc/nfc/devices.d
sudo cp /usr/share/libnfc/libnfc.conf.sample /etc/nfc/libnfc.conf
sudo cp /usr/share/libnfc/contrib/udev/93-pn53x.rules /etc/udev/rules.d/
sudo udevadm control --reload
```

## Usage
1. Run `scripts/check-nfc.sh` to verify that the CLI tools exist in `PATH` and `nfc-list --help` responds, even if no tag is present.
2. Follow the SKILL instructions (`SKILL.md`) for discovery (`nfc-list`, `nfc-taginfo`), read flows (`nfc-ndefcat`, `nfc-mfclassic`, `nfc-mfultralight`), and write flows.
3. Before writing or overwriting tag contents, confirm the UID, reader, and payload, and request the user to input `CONFIRM NFC WRITE` to guard against accidental writes.
4. Before any erase, format, or reset operation, request an additional `CONFIRM NFC FORMAT` gate even if `CONFIRM NFC WRITE` is on record; proceed only after both confirmations where both steps apply.
5. When hardware is unavailable, use `references/fallback.md` to plan record layouts and capture hex dumps so the final write can be performed once the reader returns.

## Safety
- Treat all NFC writes as destructive operations; require `CONFIRM NFC WRITE` before issuing write commands and `CONFIRM NFC FORMAT` before erase/format/reset commands, and do not proceed until each confirmation gate is explicitly satisfied.
- Redact UID/tag identifiers in user-visible output and logs by default (e.g., `[UID REDACTED]`), only revealing the full UID when the action operationally requires it, and document the reason for unmasking to preserve traceability.
- Export and store the pre-write dump (binary or hex) using the redacted donor tag reference so rollbacks remain possible without broadly exposing sensitive identifiers.
- If the reader disconnects mid-flow, re-run `nfc-list` to recover the connection string before resuming.

## Hardware notes
- Supported readers include PN532-based breakout boards, ACR122U, and most libnfc-compatible USB adapters.
- Software fallback is limited to offline planning; no emulation is bundled in this skill.

## Structure
- `SKILL.md`: Trigger/usage instructions for Codex (see skills metadata requirements).
- `README.md`: Human-oriented overview and setup guidance (this file).
- `LICENSE`: MIT license (see below).
- `scripts/check-nfc.sh`: Sanity-check script for the CLI stack.
- `references/fallback.md`: Offline planning guide for missing hardware.
