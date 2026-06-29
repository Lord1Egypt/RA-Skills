---
name: material-symbols
description: "Search, download, and generate code for Google Material Symbols icons. Use when user mentions 'material symbols', 'material icons', 'Google icons', 'Android icons', or needs to find/download icons for an app."
category: design
---

# material-symbols-cli

CLI for Google Material Symbols — search 3,900+ icons, download SVGs, generate Android Vector Drawable XML, and produce HTML/CSS code snippets.

## When To Use This Skill

Use the `material-symbols-cli` skill when you need to:

- Search icons by keyword to find the right icon name
- Download SVG icons for Android, iOS, or web projects
- Generate Android Vector Drawable XML (res/drawable/) for Android apps
- Get HTML/CSS code snippets for using Material Symbols on the web
- Browse available icon styles (outlined, rounded, sharp) and weights (100–700)

## Capabilities

- **Search icons** — Search 3,900+ Material Symbols by name (partial match, case-insensitive)
- **Get icon details** — View all available URLs for an icon (SVG, Android XML, browse link)
- **Download SVGs** — Download an icon SVG with custom style, fill state, and weight
- **Generate Android XML** — Generate Android Vector Drawable XML (20, 24, 40, 48 dp sizes)
- **Batch Android download** — Download all Android sizes for an icon into a directory
- **Generate HTML/CSS** — Get ready-to-use HTML link tags, CSS, and complete HTML pages
- **Generate CSS** — Get CSS with font-variation-settings for fill, weight, grade, and optical size
- **Generate @font-face** — Get self-hosting CSS and font download URLs
- **Browse styles** — List available icon styles (outlined, rounded, sharp)
- **Browse weights** — List available font weights (100–700) with descriptions

## Common Use Cases

- "Find an icon for search functionality in my Android app"
- "Download the settings icon as SVG for my web app"
- "Generate Android XML drawables for the home icon"
- "I need HTML code to show the menu icon on my website"
- "Get the CSS for using Material Symbols with custom weight and fill"
- "Download all sizes of the favorite icon for my Android project"
- "Search for arrow-related icons"

## Setup

If `material-symbols-cli` is not found, install and build it:
```bash
bun --version || curl -fsSL https://bun.sh/install | bash
npx api2cli bundle material-symbols
npx api2cli link material-symbols
```

`api2cli link` adds `~/.local/bin` to PATH automatically. The CLI is available in the next command.

Always use `--json` flag when calling commands programmatically.

## Working Rules

- Always use `--json` for agent-driven calls so downstream steps can parse the result.
- Start with `--help` if the exact action or flags are unclear instead of guessing.
- This CLI does not require authentication — it uses public npm/GitHub data.

## Authentication

No authentication required. Material Symbols is open source (Apache 2.0).

## Resources

### icons

Search, get info, and download Material Symbols icons.

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `icons list` | List all icons, optionally filtered by search | `--search`, `--limit`, `--fields` |
| `icons search <query>` | Search icons by keyword with details | `--limit` |
| `icons get <name>` | Get detailed info about an icon (all URLs) | — |
| `icons download <name>` | Download an icon SVG | `--style`, `--fill`, `--weight`, `--output` |
| `icons styles` | List available styles (outlined, rounded, sharp) | — |
| `icons weights` | List available weights (100–700) | — |

### android

Generate and download Android Vector Drawable XML icons.

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `android generate <name>` | Generate Android XML for an icon | `--style`, `--fill`, `--size`, `--output` |
| `android download <name>` | Download all Android XML sizes for an icon | `--style`, `--fill`, `--output-dir` |
| `android sizes` | List available Android icon sizes | — |

### compose

Generate Kotlin/Jetpack Compose code snippets.

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `compose icon <name>` | Generate a Kotlin composable function using the icon | `--style`, `--size`, `--package`, `--composable-name` |
| `compose preview <name>` | Generate a @Preview composable | `--style`, `--size` |
| `compose migration-guide` | Show migration guide from material-icons-extended to Material Symbols | — |

### code

Generate code snippets for using Material Symbols in your project.

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `code html <name>` | Generate HTML/CSS snippet | `--style`, `--fill`, `--weight`, `--grade`, `--size`, `--color` |
| `code css` | Generate CSS with font-variation-settings | `--style`, `--fill`, `--weight`, `--grade`, `--opsz` |
| `code font-face` | Generate @font-face CSS for self-hosting | `--style`, `--format` |

## Output Format

`--json` returns a standardized envelope:
```json
{ "ok": true, "data": { ... }, "meta": { "total": 42 } }
```

On error: `{ "ok": false, "error": { "message": "...", "status": 401 } }`

## Quick Reference

```bash
material-symbols-cli --help                    # List all resources and global flags
material-symbols-cli <resource> --help         # List all actions for a resource
material-symbols-cli <resource> <action> --help # Show flags for a specific action
```

```bash
# Search icons
material-symbols-cli icons list --search home --limit 10
material-symbols-cli icons search arrow --json

# Download an SVG
material-symbols-cli icons download search --style outlined --output icon.svg

# Generate Android XML
material-symbols-cli android generate search --style outlined --size 24 --output res/drawable/ic_search.xml

# Download all Android sizes
material-symbols-cli android download search --style outlined --output-dir app/src/main/res/drawable

# Generate web code
material-symbols-cli code html settings --style rounded --weight 500 --json
```

## Global Flags

All commands support: `--json`, `--format <text|json|csv|yaml>`, `--verbose`, `--no-color`, `--no-header`

Exit codes: 0 = success, 1 = API error, 2 = usage error
