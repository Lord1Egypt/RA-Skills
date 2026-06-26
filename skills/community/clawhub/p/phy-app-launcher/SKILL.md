---
name: app-launcher
description: Create macOS desktop app launchers for dev projects. Click an icon on Desktop → auto-runs local dev server in Terminal. Use when user wants to make an app "persistent", create a desktop shortcut, launch dev server with one click, or says "make this app clickable" / "create launcher" / "desktop icon for this project".
homepage: https://canlah.ai
---

# App Launcher

Create clickable macOS .app bundles that launch dev servers.

## Quick Start

```bash
python ~/.claude/skills/app-launcher/scripts/create_launcher.py /path/to/project
```

This creates `ProjectName.app` on Desktop. Double-click → Terminal opens → dev server runs.

## Usage

### Basic (Auto-detect)
```bash
python ~/.claude/skills/app-launcher/scripts/create_launcher.py ~/projects/my-app
```

### With Custom Options
```bash
python ~/.claude/skills/app-launcher/scripts/create_launcher.py ~/projects/my-app \
  --name "My App" \
  --cmd "npm run dev" \
  --icon ~/icons/my-app.png \
  --output ~/Desktop
```

## Options

| Option | Description |
|--------|-------------|
| `--name` | App display name (default: folder name) |
| `--cmd` | Start command (default: auto-detect) |
| `--icon` | Icon file path (.icns or .png) |
| `--output` | Output directory (default: ~/Desktop) |

## Auto-Detection

The script auto-detects project type:

| Project | Detection | Default Command |
|---------|-----------|-----------------|
| Node.js | `package.json` | `npm run dev` / `npm start` |
| Python | `app.py` / `main.py` | `python app.py` |
| Django | `manage.py` | `python manage.py runserver` |
| Docker | `docker-compose.yml` | `docker-compose up` |
| Make | `Makefile` | `make dev` |

Also auto-detects `venv/` or `.venv/` and activates it.

## Custom Icon

Provide a .png or .icns file:
```bash
--icon ~/Desktop/my-logo.png
```

The script converts PNG to proper macOS icns format.

## Workflow

1. User says "create launcher for this project" or "make desktop icon"
2. Identify project path and any custom requirements (name, icon, command)
3. Run the script with appropriate options
4. Confirm the .app was created on Desktop
5. User can now double-click to launch

## Examples

### Create launcher for current project
```bash
python ~/.claude/skills/app-launcher/scripts/create_launcher.py .
```

### Create launcher with custom icon from project
```bash
python ~/.claude/skills/app-launcher/scripts/create_launcher.py ~/projects/canmarket \
  --name "CanMarket Dev" \
  --icon ~/projects/canmarket/public/logo.png
```

### Create launcher with specific command
```bash
python ~/.claude/skills/app-launcher/scripts/create_launcher.py ~/projects/api \
  --cmd "uvicorn main:app --reload"
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
