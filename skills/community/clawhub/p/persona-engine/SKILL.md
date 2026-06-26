# AI Persona Engine

**Skill Name:** ai-persona-engine
**Version:** 2.0
**Author:** SPFAdvisors

Create a fully realized AI persona — voice, face, personality, and memory — in under 5 minutes.

---

## Quick Start

```bash
# Install from ClawHub
clawhub install ai-persona-engine

# Create your first persona
openclaw persona create

# That's it. The wizard handles everything.
```

---

## Commands

### `persona create`

Interactive wizard that walks through persona creation step by step.

```bash
openclaw persona create

# With flags
openclaw persona create --dry-run          # Show what would be generated
openclaw persona create --workspace=~/.openclaw/workspace-new
```

The wizard covers 7 steps:

1. **Name & Identity** — name, emoji, description, nickname
2. **Personality** — archetype selection, blending, communication style, relationship boundaries
3. **Voice** — provider selection (ElevenLabs, Grok TTS, built-in), voice testing
4. **Visual Identity** — appearance description, reference image generation
5. **Your Context** — USER.md with your name, timezone, preferences
6. **Memory** — daily notes, long-term curation, heartbeat maintenance
7. **Platforms** — channel selection and per-channel behavior

Output: SOUL.md, USER.md, IDENTITY.md, MEMORY.md, AGENTS.md, HEARTBEAT.md, and updated openclaw.json.

### `persona update`

Modify specific persona fields without re-running the full wizard. Includes safe update pipeline with automatic backup and diff preview.

```bash
# Update voice provider
openclaw persona update --voice-provider elevenlabs --voice-id abc123

# Add or remove personality traits
openclaw persona update --add-trait "sarcastic" --remove-trait "formal"

# Update appearance and regenerate reference image
openclaw persona update --appearance "new description..." --regen-image

# Regenerate SOUL.md from current config (with backup + diff)
openclaw persona update --regen-soul

# Force regeneration (skip diff review)
openclaw persona update --regen-soul --force

# Interactive mode (step-by-step, choose what to change)
openclaw persona update -i
```

**Safe Update Pipeline:** Before any `--regen` operation, the tool:
1. Creates `.persona-backup/` with current files
2. Regenerates the target file
3. Shows a diff of what changed
4. Asks for confirmation (or use `--force` to skip)

### `persona export`

Package the persona into a portable `.persona` bundle.

```bash
# Basic export (no memory, no API keys)
openclaw persona export

# Include memory files
openclaw persona export --name pepper-backup --include-memory

# Include voice config (still excludes API keys)
openclaw persona export --include-voice-config

# Export from a specific workspace
openclaw persona export --workspace ~/.openclaw/workspace-ultron
```

### `persona import`

Import a `.persona` bundle into a workspace.

```bash
# Interactive import (confirms each file)
openclaw persona import pepper.persona

# Import into a specific workspace
openclaw persona import pepper.persona --workspace ~/.openclaw/workspace-new

# Overwrite existing files without prompting
openclaw persona import pepper.persona --force
```

### `persona preview`

Generate sample conversations showing how the persona would respond. Template-based, no LLM calls.

```bash
# Preview from config
python3 scripts/persona-preview.py --archetype companion --name "Pepper" --emoji "🌶️"

# Preview from workspace
python3 scripts/persona-preview.py --workspace ~/.openclaw/workspace

# Preview from profile JSON
python3 scripts/persona-preview.py --input persona-config.json
```

Shows 4 scenarios: greeting, asking for help, user mistake, emotional moment.

### `persona migrate`

Reverse-engineer a persona config from existing workspace files.

```bash
# Migrate workspace to config JSON
python3 scripts/persona-migrate.py --workspace ~/.openclaw/workspace

# Output to file
python3 scripts/persona-migrate.py --workspace ~/.openclaw/workspace --output persona-config.json
```

See [references/migration-guide.md](references/migration-guide.md) for detailed migration instructions.

### `persona validate`

Check workspace for missing or malformed persona files.

```bash
python3 scripts/persona-validate.py --workspace ~/.openclaw/workspace

# With config validation
python3 scripts/persona-validate.py --workspace ~/.openclaw/workspace --config ~/.openclaw/openclaw.json

# JSON output for scripting
python3 scripts/persona-validate.py --workspace ~/.openclaw/workspace --json
```

### `persona diff`

Compare current workspace files against what the generator would produce.

```bash
python3 scripts/persona-diff.py --workspace ~/.openclaw/workspace --config ~/.openclaw/openclaw.json
```

### `persona list`

List all personas across workspaces.

```bash
python3 scripts/persona-list.py

# JSON output
python3 scripts/persona-list.py --json
```

### `persona fleet`

Show a fleet view of all agents across machines.

```bash
python3 scripts/persona-fleet.py

# JSON output
python3 scripts/persona-fleet.py --json
```

### `voice audition`

Audition multiple voices for a provider.

```bash
# List ElevenLabs voices
python3 scripts/voice-setup.py --audition --provider elevenlabs

# Filter by gender
python3 scripts/voice-setup.py --audition --provider elevenlabs --gender female

# List built-in voices
python3 scripts/voice-setup.py --audition --provider builtin
```

---

## Personality Blending

Create hybrid personalities by blending multiple archetypes with weighted percentages.

```bash
# During wizard: choose "Blend with a second archetype" option
openclaw persona create

# Programmatically:
cat > blend-profile.json << 'EOF'
{
    "name": "Muse",
    "emoji": "🎨",
    "archetypes": [
        {"name": "companion", "weight": 0.7},
        {"name": "creative", "weight": 0.3}
    ]
}
EOF
python3 scripts/generate-soul.py --input blend-profile.json --output SOUL.md
```

Blending merges:
- **Traits**: Combined from both profiles, weighted by presence
- **Brevity**: Weighted average (e.g., 0.7×3 + 0.3×4 = 3.3 → 3)
- **Emotional depth**: Weighted average mapped to levels
- **Vibe summaries**: Concatenated from both profiles
- **Platform notes**: Combined, deduplicated

---

## Community Templates

Pre-built personality profiles for common use cases in `assets/community-templates/`:

| Template | Description |
|----------|-------------|
| `financial-advisor` | Informed, cautious, data-driven financial guide |
| `fitness-coach` | Motivating, knowledgeable, encouraging workout companion |
| `kids-tutor` | Patient, fun, age-appropriate learning buddy (ages 6-12) |
| `creative-writer` | Lyrical, perceptive collaborative writing partner |
| `sales-rep` | Persuasive, empathetic, goal-oriented sales professional |
| `therapist` | Empathetic, boundaried emotional wellness companion |
| `gaming-buddy` | Enthusiastic, strategic, competitive gaming partner |
| `executive-assistant` | Anticipatory, discreet, ultra-efficient EA |

Use community templates directly or blend them with built-in archetypes:

```bash
python3 scripts/generate-soul.py --archetype therapist --name "Sage" --emoji "🧘"
```

---

## File Structure

```
ai-persona-engine/
├── SKILL.md                     # This file
├── DESIGN.md                    # Full design document
├── scripts/
│   ├── persona-create.sh        # Setup wizard (v2: blending, --dry-run, --workspace)
│   ├── persona-update.sh        # Field updater (v2: safe update pipeline)
│   ├── persona-export.sh        # Bundle exporter (v2: cross-workspace)
│   ├── persona-import.sh        # Bundle importer (v2: cross-workspace)
│   ├── persona-preview.py       # [NEW] Sample conversation generator
│   ├── persona-migrate.py       # [NEW] Reverse-engineer config from workspace
│   ├── persona-validate.py      # [NEW] Workspace validation
│   ├── persona-diff.py          # [NEW] Diff workspace vs generated
│   ├── persona-list.py          # [NEW] List all personas across workspaces
│   ├── persona-fleet.py         # [NEW] Fleet view of all agents
│   ├── generate-soul.py         # SOUL.md generator (v2: blending support)
│   ├── generate-user.py         # USER.md generator
│   ├── generate-identity.py     # IDENTITY.md generator
│   ├── generate-memory.py       # MEMORY.md + memory/ scaffolding
│   ├── voice-setup.py           # Voice provider config (v2: --audition)
│   ├── image-setup.py           # Image provider config + reference image
│   └── lib/
│       ├── providers.py         # Provider abstraction layer
│       ├── templates.py         # Template engine + personality blending
│       ├── config.py            # openclaw.json helpers
│       └── prompts.py           # Wizard prompt definitions
├── references/
│   ├── voice-providers.md       # Voice provider setup guide
│   ├── image-providers.md       # Image provider setup guide
│   ├── personality-archetypes.md # Archetype reference
│   ├── soul-writing-guide.md    # SOUL.md writing tips
│   ├── config-schema.md         # openclaw.json schema reference
│   └── migration-guide.md       # [NEW] Migration guide for existing users
├── assets/
│   ├── personality-profiles/    # JSON presets per archetype (5 built-in)
│   ├── community-templates/     # [NEW] 8 community personality profiles
│   └── templates/               # Handlebars templates for generated files
└── tests/
    ├── test-generators.py       # 77 unit tests (v2: blending, migration, etc.)
    ├── test-wizard.sh
    └── test-export-import.sh
```

---

## Configuration

The persona engine adds a `persona` section to `openclaw.json`. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `persona.name` | string | Agent's display name |
| `persona.emoji` | string | Agent's emoji identifier |
| `persona.identity` | object | Creature type, vibe, nickname |
| `persona.voice` | object | Voice provider and settings |
| `persona.image` | object | Image provider and canonical look |
| `persona.personality` | object | Archetype, traits, communication style |
| `persona.personality.archetypes` | array | [NEW] Blend sources with weights |
| `persona.memory` | object | Memory capture and curation settings |

See [references/config-schema.md](references/config-schema.md) for the full schema.

---

## Dependencies

**Required:**
- OpenClaw (any version with skill support)
- Python 3.9+
- Node.js 22+

**Optional (based on chosen providers):**
- ElevenLabs API key (voice)
- Gemini API key (image generation)
- xAI API key (Grok TTS / Grok Imagine)
- ffmpeg (audio format conversion for WhatsApp voice messages)

---

## Further Reading

- [Voice Providers Guide](references/voice-providers.md)
- [Image Providers Guide](references/image-providers.md)
- [Personality Archetypes](references/personality-archetypes.md)
- [SOUL.md Writing Guide](references/soul-writing-guide.md)
- [Config Schema Reference](references/config-schema.md)
- [Migration Guide](references/migration-guide.md)
- [Design Document](DESIGN.md)
