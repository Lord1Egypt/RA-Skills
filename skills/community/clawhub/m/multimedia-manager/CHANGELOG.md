# Changelog

## [1.0.6] - 2026-03-17

### Bug Fix

- Fixed `NameError: lat` in `image_import.py` — GPS extraction was happening after the variable was referenced. Moved EXIF GPS extraction before AI GPS fallback logic
- Corrected `not lat` to `lat is None` for proper None check

## [1.0.5] - 2026-03-17

### Transparency Improvement

- Added **Behavior Transparency** section in SKILL.md documenting all scanner-flagged behaviors:
  - `setup.sh` pip install (with manual alternative)
  - `.env` file reading (standard dotenv pattern)
  - `cleanup_inbound.py` file deletion (scoped to vault/inbound only)
  - Subprocess calls for ffmpeg/ffprobe (optional, graceful degradation)

## [1.0.4] - 2026-03-17

### Security & Documentation Fix

- Declared **all 5** environment variables in SKILL.md: added `IMAGE_VAULT_DB` and `PORT` (previously undeclared but used in code)
- Updated `.env.example` to document all 5 variables as a ready-to-copy template
- Fixed misleading "no network after install" — now clarifies `setup.sh` performs a one-time `pip install` requiring network
- Removed duplicate Configuration section in SKILL.md
- Changed wording to "These are the only environment variables read by this skill"

## [1.0.3] - 2026-03-17

### Security Fix

- Removed hardcoded `~/.openclaw` path from `cleanup_inbound.py` — now uses configurable `--dir` parameter with `IMAGE_VAULT_DIR/inbound` as default
- Removed `ngrok` section from `config.example.yaml` and `config.yaml` (ngrok is a Pro-only feature)
- Added explicit **Environment Variables** declaration table in SKILL.md listing all 3 env vars used
- No undeclared environment variable usage

## [1.0.1] - 2026-03-17

### Security & Compliance

- Default server bind changed from `0.0.0.0` to `127.0.0.1` (localhost only)
- Added `Security & Permissions` section to SKILL.md
- Setup script now displays clear explanation of what it installs
- Removed references to Pro-only features from community .env.example
- Fixed `init_db()` call in setup.sh

## [1.0.0] - 2026-03-17

### Initial Release (Community Edition)

**Core Features**
- Image and video import with auto-deduplication (SHA256)
- SQLite-backed metadata store with FTS5 full-text search
- Auto-generated thumbnails (WebP)
- Category system: ai-generated, family, screenshots, covers, templates, uncategorized
- CLI tool for import, search, describe, and stats

**Web Gallery**
- Responsive gallery with search and filtering
- Favorites and albums
- Token-based authentication
- Dark theme UI

**Developer Experience**
- Environment-based configuration (`.env` + `config.yaml`)
- One-command setup (`bash setup.sh`)
- Only 3 dependencies: Flask, Pillow, PyYAML
