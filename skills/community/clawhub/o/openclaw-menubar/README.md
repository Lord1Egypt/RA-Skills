# OpenClaw Menu Bar Skill

A skill that enables OpenClaw as a native macOS menu bar app with quick access popup.

## For Users

### Install the Skill

1. Download `menubar.skill` file
2. Install it: `openclaw skill install menubar.skill`
3. Enable it by saying: **"enable menubar"** to OpenClaw

Or manually:
```bash
cd ~/.openclaw/workspace/skills/menubar
scripts/install.sh
scripts/start.sh
```

### Usage

Once enabled, you'll see a 🦀 crab icon in your macOS menu bar:
- **Click** the icon to open quick chat popup
- **Cmd+Shift+O** keyboard shortcut to toggle
- **Click outside** or press Esc to hide

### Stop

Say **"disable menubar"** to OpenClaw, or manually:
```bash
cd ~/.openclaw/workspace/skills/menubar
scripts/stop.sh
```

## For Developers

### Local Development

The skill is already set up at `/Users/prabhanjansharma/.openclaw/workspace/skills/menubar`

To test locally:
```bash
cd /Users/prabhanjansharma/.openclaw/workspace/skills/menubar
scripts/install.sh
scripts/start.sh
```

### Making Changes

1. Edit files in `skills/menubar/assets/openclaw-menubar/`
2. Restart: `scripts/stop.sh && scripts/start.sh`
3. Repackage when ready: `python3 /usr/local/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py skills/menubar`

### Distribution

The packaged skill is at: `/Users/prabhanjansharma/.openclaw/workspace/menubar.skill`

Share this file with other OpenClaw users - they can install it with:
```bash
openclaw skill install menubar.skill
```

## What's Inside

```
menubar/
├── SKILL.md              # Skill instructions for OpenClaw
├── scripts/
│   ├── install.sh        # Install dependencies
│   ├── start.sh          # Launch menu bar app
│   ├── stop.sh           # Stop menu bar app
│   └── status.sh         # Check if running
└── assets/
    └── openclaw-menubar/ # Complete Electron app
        ├── main.js       # Electron main process
        ├── index-webchat.html # Custom header
        ├── icons/        # Crab icon (22x22, 44x44)
        └── package.json  # Dependencies
```

## Requirements

- macOS (menu bar apps are macOS-specific)
- OpenClaw Gateway running
- Node.js for Electron

## Customization

See SKILL.md for customization options (icon, window size, keyboard shortcut).
