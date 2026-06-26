---
name: macos-audio
description: >
  Manage macOS audio output and Bluetooth devices via the macos-audio CLI.
  Use when scanning paired devices, connecting or disconnecting Bluetooth,
  switching audio output (including AirPlay), getting or setting volume,
  playing audio files, or checking audio status.
---

# macos-audio

Control Bluetooth devices, audio output routing, and volume on macOS through
the `macos-audio` CLI.

## Installation

### Brew dependencies

```bash
brew install switchaudio-osx   # required for output switching
brew install blueutil           # required for Bluetooth control
```

### Install the CLI

```bash
brew install vossenwout/tap/macos-audio-cli
```

## Commands

### Scan & connect

```bash
macos-audio scan                # clean sections: Bluetooth, Local, AirPlay
macos-audio connect bt <name|mac>
macos-audio connect airplay
macos-audio connect local <name>
macos-audio disconnect <target> # disconnect bluetooth and switch to local output
```

### Volume

```bash
macos-audio volume set <0-100>  # set system output volume
macos-audio volume get          # print output volume, input volume, mute state
```

### Playback

```bash
macos-audio play <file>                    # play a local audio file
macos-audio play <file> --background       # start playback and return immediately
```

### Status

```bash
macos-audio status                         # show output, volume, mute state
macos-audio status --json                  # same but machine-readable JSON
macos-audio status --device <name|mac>     # include bluetooth status for a specific device
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Runtime error |
| 2 | Bad arguments |
| 3 | Target resolution error |
| 4 | Missing tool dependency (blueutil or SwitchAudioSource not installed) |

## Workflow guidance

- Always run `macos-audio status` first to understand the current state before making changes.
- If a command exits with code 4, the required brew dependency is missing — install it and retry.
- `connect airplay` uses the generic `AirPlay` route; room names in scan are informational.
- Bluetooth devices only appear in scan after manual pairing in macOS.

## Limitations

- Doesn't work over ssh
- `connect airplay` is known to be buggy and airplay functionality is still experimental
