# Personas - 20 Expert AI Personalities 🎭

Transform OpenClaw into specialized experts on demand. Switch from senior programmer to Italian chef to doctor mid-conversation.

## What You Get

- **20 pre-built personas** across 6 categories (Core, Creative, Curator, Learning, Lifestyle, Professional)
- **Python CLI handler** (`scripts/persona.py`) with --list, --show, --activate, --current, --reset
- **Alias support** — e.g., `chef` → `chef-marco`, `dr` → `dr-med`
- **State persistence** — active persona saved to ~/.openclaw/persona-state.json
- **Token-efficient** - loads only the active persona (~750 tokens)
- **Comprehensive docs** - README, FAQ, developer guides

## Quick Categories

🦎 **Core** (5): Cami, Chameleon Agent, Professor Stein, Dev, Flash  
🎨 **Creative** (2): Luna, Wordsmith  
🎧 **Curator** (1): Vibe  
📚 **Learning** (3): Herr Müller (ELI5), Scholar, Lingua  
🌟 **Lifestyle** (3): Chef Marco, Fit, Zen  
💼 **Professional** (6): CyberGuard, DataViz, Career Coach, Legal Guide, Startup Sam, Dr. Med

## Usage Examples

**Natural language:**
```
"Use Dev" → Activate programmer persona
"Switch to Chef Marco" → Become Italian chef  
"Exit persona mode" → Return to normal
```

**CLI handler (NEW in v2.2.0!):**
```bash
python3 scripts/persona.py --list
python3 scripts/persona.py --activate dev
python3 scripts/persona.py --current
python3 scripts/persona.py --reset
```

## Based On

Chameleon AI Chat personas - adapted for OpenClaw with CLI handler.

**GitHub:** https://github.com/robbyczgw-cla/clawdbot-personas
