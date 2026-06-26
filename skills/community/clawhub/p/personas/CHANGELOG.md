# Changelog

## [2.2.3] - 2026-02-11

### Changed

- **INTERNAL.md Security section:** Reworded security/safety language to be neutral and implementation-focused.
- Removed explicit "prompt injection risks" threat framing from the internal documentation text.

## [2.2.2] - 2026-02-11

### 🆕 Python CLI Handler

Added `scripts/persona.py` for programmatic persona management:

#### Features
- `--list` — List all available personas
- `--show <name>` — Show persona details
- `--activate <name>` — Activate a persona (outputs system prompt, saves state)
- `--current` — Show currently active persona
- `--reset` — Deactivate/reset to default

#### Alias Support
Common variations are now supported:
- `chef` → `chef-marco`
- `dr` → `dr-med`
- `professor` → `professor-stein`
- And more...

#### State Persistence
Active persona is saved to `~/.openclaw/persona-state.json` and persists across sessions.

#### History Tracking
Activation history is tracked for easy switching back.

### Fixed
- **Persona Count:** Documentation now correctly states 20 personas (not 31)
- **Path References:** Removed hardcoded paths, use relative paths

### Usage Examples
```bash
# List all personas
python3 scripts/persona.py --list

# Activate a persona
python3 scripts/persona.py --activate dev

# Check current
python3 scripts/persona.py --current

# Reset
python3 scripts/persona.py --reset
```

## [2.1.1] - 2026-02-04

- Privacy cleanup: removed hardcoded paths and personal info from docs
