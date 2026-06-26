# Installation Reference

Run installation commands only after explicit user approval.

## Option 1: Homebrew (macOS/Linux)

```bash
brew install philipp-eisen/tap/padel-tui
padel-tui --version
```

## Option 2: Prebuilt Binary

1. Download the archive from GitHub releases.
2. Extract and verify:

```bash
tar -xzf padel-tui-<version>-<platform>.tar.gz
chmod +x padel-tui
./padel-tui --version
```

Add binary to `PATH` to use `padel-tui` globally.

## Option 3: Run From Source

```bash
bun install
./bin/padel-tui --version
```

Use source command prefix:

```bash
./bin/padel-tui <command>
```

## First Login

```bash
padel-tui auth login
```

Complete email/password prompts in the terminal. Do not pass credentials inline.

Default session file: `~/.config/padel-tui/session.json`.
