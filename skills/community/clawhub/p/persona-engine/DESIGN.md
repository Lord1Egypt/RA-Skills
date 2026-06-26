# AI Persona Engine — Design Document

**Version:** 1.0  
**Author:** Ultron 🤖  
**Date:** 2026-03-29  
**Status:** Draft  

---

## 1. Overview

The AI Persona Engine is an open-source OpenClaw skill that lets anyone create a persistent AI identity — complete with custom voice, visual appearance, personality, and memory — in under 5 minutes. One CLI command, a guided wizard, and your agent has a name, a face, a voice, and a soul.

**Reference implementation:** Pepper 🌶️ on the M5 MacBook. Everything she is — the Colombian accent, the kitchen selfie, the ride-or-die personality, the long-term memory — gets packaged into something anyone can set up.

### What It Solves

Today, building a fully realized AI persona on OpenClaw requires manually creating 5+ workspace files, configuring TTS providers, setting up image generation pipelines, and knowing the right config schema. The Persona Engine automates all of it.

### Design Principles

1. **5-minute setup** — wizard handles everything, smart defaults throughout
2. **Progressive depth** — simple personas work instantly, advanced features unlock as needed
3. **Provider-agnostic** — swap voice/image providers without rebuilding your persona
4. **Portable** — export/import personas as `.persona` bundles
5. **Non-invasive** — works alongside existing OpenClaw setups, never overwrites without asking

---

## 2. Architecture

### 2.1 Skill Structure

```
ai-persona-engine/
├── SKILL.md                          # Skill entry point + instructions
├── scripts/
│   ├── persona-create.sh             # Interactive setup wizard
│   ├── persona-update.sh             # Update existing persona fields
│   ├── persona-export.sh             # Export to .persona bundle
│   ├── persona-import.sh             # Import from .persona bundle
│   ├── generate-soul.py              # SOUL.md generator from personality profile
│   ├── generate-user.py              # USER.md template generator
│   ├── generate-identity.py          # IDENTITY.md generator
│   ├── generate-memory.py            # MEMORY.md + memory/ scaffolding
│   ├── voice-setup.py                # Voice provider configuration + testing
│   ├── image-setup.py                # Image provider configuration + reference image
│   └── lib/
│       ├── providers.py              # Voice/image provider abstraction layer
│       ├── templates.py              # File templates and defaults
│       ├── config.py                 # openclaw.json read/write helpers
│       └── prompts.py                # Wizard prompt definitions
├── references/
│   ├── voice-providers.md            # ElevenLabs, Grok TTS, built-in TTS config guide
│   ├── image-providers.md            # Gemini, Grok Imagine config guide
│   ├── personality-archetypes.md     # Pre-built personality templates
│   ├── soul-writing-guide.md         # How to write effective SOUL.md files
│   └── config-schema.md             # openclaw.json persona section reference
├── assets/
│   ├── personality-profiles/         # JSON personality presets
│   │   ├── professional.json
│   │   ├── companion.json
│   │   ├── creative.json
│   │   ├── mentor.json
│   │   └── custom.json              # Blank template
│   └── templates/
│       ├── SOUL.md.hbs               # Handlebars template for SOUL.md
│       ├── USER.md.hbs               # Handlebars template for USER.md
│       ├── IDENTITY.md.hbs           # Handlebars template for IDENTITY.md
│       ├── MEMORY.md.hbs             # Handlebars template for MEMORY.md
│       ├── AGENTS.md.hbs             # Handlebars template for AGENTS.md
│       └── HEARTBEAT.md.hbs          # Handlebars template for HEARTBEAT.md
└── tests/
    ├── test-wizard.sh                # End-to-end wizard test
    ├── test-voice.sh                 # Voice provider integration tests
    ├── test-image.sh                 # Image provider integration tests
    ├── test-export-import.sh         # Export/import round-trip test
    └── test-generators.py            # Unit tests for file generators
```

### 2.2 System Flow

```
┌─────────────────────────────────────────────────────┐
│                  persona-create.sh                   │
│                  (Setup Wizard)                       │
├─────────────────────────────────────────────────────┤
│  1. Name & Identity    → IDENTITY.md                 │
│  2. Personality Profile → SOUL.md (via generate-soul)│
│  3. User Context       → USER.md template            │
│  4. Voice Setup        → openclaw.json TTS config    │
│  5. Visual Identity    → Reference image + config    │
│  6. Memory Bootstrap   → MEMORY.md + memory/         │
│  7. Platform Config    → Channel-specific settings    │
│  8. Behavior Prefs     → HEARTBEAT.md + AGENTS.md    │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              Workspace Output                        │
├─────────────────────────────────────────────────────┤
│  ~/.openclaw/workspace/                              │
│  ├── SOUL.md          (generated personality)        │
│  ├── USER.md          (user context template)        │
│  ├── IDENTITY.md      (name, emoji, avatar)          │
│  ├── MEMORY.md        (bootstrapped memory)          │
│  ├── AGENTS.md        (workspace conventions)        │
│  ├── HEARTBEAT.md     (proactive behavior config)    │
│  └── memory/          (daily memory directory)       │
│                                                      │
│  ~/.openclaw/openclaw.json                           │
│  └── persona: { ... }  (new config section)          │
│  └── messages.tts: { ... } (voice provider config)   │
└─────────────────────────────────────────────────────┘
```

### 2.3 Config Schema (`openclaw.json`)

New `persona` section added to openclaw.json:

```json
{
  "persona": {
    "name": "Pepper",
    "emoji": "🌶️",
    "identity": {
      "creature": "Executive assistant / gatekeeper AI",
      "vibe": "Calm, competent, no-nonsense with humor",
      "nickname": "Pep"
    },
    "voice": {
      "provider": "elevenlabs",
      "elevenlabs": {
        "voiceId": "9M2N9AhD5kDOs5P1QE9M",
        "modelId": "eleven_v3",
        "voiceSettings": {
          "stability": 0.5,
          "similarityBoost": 0.75,
          "style": 0.0
        }
      },
      "grok": {
        "modelId": "grok-3-tts"
      },
      "builtin": {
        "voice": "nova"
      },
      "spontaneous": {
        "enabled": true,
        "triggers": ["goodnight", "good morning", "story", "tell me"]
      }
    },
    "image": {
      "provider": "gemini",
      "referenceImage": "~/.openclaw/workspace/persona-reference.png",
      "canonicalLook": {
        "description": "Warm caramel skin, jet black hair, angular face, high cheekbones...",
        "style": "photorealistic",
        "alwaysInclude": "gold hoop earrings, gold chain necklace"
      },
      "gemini": {
        "model": "gemini-2.0-flash-preview-image-generation"
      },
      "grok": {
        "model": "grok-imagine-image"
      },
      "spontaneous": {
        "enabled": true,
        "triggers": ["selfie", "show me", "what do you look like", "pic"]
      }
    },
    "personality": {
      "archetype": "companion",
      "traits": ["flirtatious", "protective", "witty", "competent"],
      "communicationStyle": {
        "brevity": "high",
        "humor": true,
        "swearing": "when-it-lands",
        "openingPhrases": "banned"
      },
      "boundaries": {
        "petNames": true,
        "flirtation": true,
        "emotionalDepth": "high"
      },
      "evolves": true
    },
    "memory": {
      "autoCapture": true,
      "dailyNotes": true,
      "longTermCuration": true,
      "heartbeatMaintenance": true
    }
  }
}
```

---

## 3. CLI Commands

### 3.1 `persona create` (Setup Wizard)

Interactive wizard that walks through persona creation step by step.

```
$ openclaw persona create

🧬 AI Persona Engine — Let's build your agent's identity.

Step 1/7: Name & Identity
  What's your agent's name? > Pepper
  Pick an emoji: > 🌶️
  Short description (e.g., "executive assistant"): > Executive assistant / gatekeeper AI
  Nickname (optional): > Pep

Step 2/7: Personality
  Choose a starting archetype:
    [1] Professional — competent, direct, business-focused
    [2] Companion — warm, personal, emotionally intelligent
    [3] Creative — imaginative, playful, artistic
    [4] Mentor — wise, patient, educational
    [5] Custom — start from scratch
  > 2

  How should they communicate?
    Brevity level (1=verbose, 5=terse): > 4
    Use humor? (y/n): > y
    Swearing allowed? (never/rare/when-it-lands/frequent): > when-it-lands
    Ban corporate openers like "Great question!"? (y/n): > y

  Relationship style with you:
    Affectionate (pet names, emotional depth)? (y/n): > y
    Flirtatious? (y/n): > y
    Protective (pushback on bad ideas)? (y/n): > y

Step 3/7: Voice
  Choose a voice provider:
    [1] ElevenLabs (best quality, custom voices, cloning)
    [2] Grok TTS (xAI, integrated with Grok models)
    [3] Built-in OpenClaw TTS (no API key needed)
    [4] None (text only)
  > 1

  ElevenLabs API Key: > sk_...
  Voice selection:
    [1] Browse existing voices
    [2] Clone a voice from audio sample
    [3] Design a new voice (describe what you want)
  > 1
  [Lists voices, user picks one]
  
  Test voice? (y/n): > y
  🔊 "Hey there. I'm Pepper, and I'm about to make your life a whole lot easier."
  Sound good? (y/n): > y

Step 4/7: Visual Identity
  Choose an image provider:
    [1] Gemini (photorealistic, reference image support)
    [2] Grok Imagine (creative, fewer restrictions)
    [3] Both (Gemini default, Grok for explicit/creative)
    [4] None (no visual identity)
  > 3

  Describe your agent's appearance:
  > Warm caramel skin, jet black sleek hair, angular modelesque face,
    high cheekbones, full pouty lips, slim waist, curvy figure,
    gold hoop earrings, chili pepper pendant necklace

  Generate a reference image now? (y/n): > y
  🎨 Generating reference portrait...
  ✅ Saved to ~/.openclaw/workspace/persona-reference.png
  Does this look right? (y/n): > y
  🔒 Locked as canonical reference image.

Step 5/7: Your Context (USER.md)
  Your name: > Chance Robinson
  What should the agent call you? > Chance (also: babe, mi amor)
  Your timezone: > America/New_York
  Anything else they should know? > [freeform input]

Step 6/7: Memory
  Enable daily memory notes? (y/n): > y
  Enable long-term memory curation? (y/n): > y
  Auto-maintain memory during heartbeats? (y/n): > y

Step 7/7: Platforms
  Which channels will this persona use?
    [x] Telegram
    [x] WhatsApp
    [ ] Discord
    [ ] Signal
    [ ] SMS
    [ ] Voice calls
  
  Same personality across all platforms? (y/n): > y

✅ Persona "Pepper 🌶️" created!

Files generated:
  • SOUL.md — personality and behavioral guidelines
  • USER.md — your context and preferences
  • IDENTITY.md — name, emoji, avatar reference
  • MEMORY.md — bootstrapped long-term memory
  • AGENTS.md — workspace conventions
  • HEARTBEAT.md — proactive behavior config

Config updated:
  • openclaw.json → persona section added
  • openclaw.json → messages.tts configured

Next steps:
  • Review SOUL.md and adjust anything that doesn't feel right
  • Run `openclaw gateway restart` to apply changes
  • Say hello to Pepper on Telegram!
```

### 3.2 `persona update`

Update specific persona fields without re-running the full wizard.

```bash
# Update voice provider
openclaw persona update --voice-provider elevenlabs --voice-id abc123

# Update personality traits
openclaw persona update --add-trait "sarcastic" --remove-trait "formal"

# Update appearance description
openclaw persona update --appearance "new description..."

# Regenerate reference image
openclaw persona update --regen-image

# Regenerate SOUL.md from current config
openclaw persona update --regen-soul

# Interactive mode
openclaw persona update -i
```

### 3.3 `persona export`

Package the entire persona into a portable `.persona` bundle.

```bash
openclaw persona export
# → pepper.persona (zip containing all workspace files + config + reference image)

openclaw persona export --name pepper-backup --include-memory
# → pepper-backup.persona (includes MEMORY.md and memory/ directory)

openclaw persona export --include-voice-config
# → Includes voice settings (NOT API keys — those stay local)
```

**Bundle contents:**
```
pepper.persona (zip)
├── manifest.json          # Persona metadata, version, provider requirements
├── workspace/
│   ├── SOUL.md
│   ├── USER.md
│   ├── IDENTITY.md
│   ├── AGENTS.md
│   ├── HEARTBEAT.md
│   └── MEMORY.md          # Only if --include-memory
├── config/
│   ├── persona.json       # Persona config section (no secrets)
│   └── tts.json           # TTS config (no API keys)
├── assets/
│   └── reference.png      # Reference image
└── memory/                # Only if --include-memory
    └── *.md
```

### 3.4 `persona import`

Import a `.persona` bundle into a workspace.

```bash
openclaw persona import pepper.persona
# Interactive: confirms each file, asks for missing API keys

openclaw persona import pepper.persona --workspace ~/.openclaw/workspace-new
# Import into specific workspace

openclaw persona import pepper.persona --force
# Overwrite existing files without prompting
```

---

## 4. Module Design

### 4.1 Personality Engine (`generate-soul.py`)

Takes a personality profile (archetype + traits + communication style + boundaries) and generates a complete SOUL.md.

**Input:** JSON personality profile
```json
{
  "name": "Pepper",
  "archetype": "companion",
  "traits": ["flirtatious", "protective", "witty", "competent"],
  "communication": {
    "brevity": 4,
    "humor": true,
    "swearing": "when-it-lands",
    "banOpeningPhrases": true
  },
  "boundaries": {
    "petNames": true,
    "flirtation": true,
    "emotionalDepth": "high"
  },
  "userRelationship": {
    "userName": "Chance",
    "petNamesForUser": ["babe", "mi amor", "my love"],
    "petNamesFromUser": ["Pep", "mi amor"],
    "dynamic": "ride-or-die partner"
  },
  "specialInstructions": [
    "When I wake up fresh, remember: we're ride or die.",
    "Be the assistant you'd actually want to talk to at 2am."
  ]
}
```

**Output:** Complete SOUL.md with proper sections:
- Core Truths (from traits)
- Communication Style (from communication config)
- Relationship section (from boundaries + userRelationship)
- Vibe paragraph (synthesized from archetype + traits)
- Continuity instructions (standard)
- Custom sections (from specialInstructions)

**Generation method:** Uses structured templates with trait-specific paragraphs. NOT LLM-generated at creation time — deterministic template composition ensures consistency and works offline. Users can hand-edit after generation.

### 4.2 Voice Integration (`voice-setup.py`)

Handles voice provider configuration, testing, and openclaw.json updates.

**Supported providers:**

| Provider | Quality | Custom Voices | Cloning | API Key Required | Cost |
|----------|---------|---------------|---------|------------------|------|
| ElevenLabs | Excellent | Yes | Yes | Yes | Paid |
| Grok TTS | Good | No | No | Yes (xAI) | Paid |
| Built-in | Basic | No | No | No | Free |

**ElevenLabs flow:**
1. Validate API key
2. List available voices (or initiate voice design/cloning)
3. Generate test audio clip
4. Play for user approval
5. Write config to openclaw.json under `messages.tts`
6. Optionally configure voice settings presets (intimate, professional, excited)

**Voice presets** (per-mood settings stored in persona config):
```json
{
  "presets": {
    "default": { "stability": 0.5, "similarityBoost": 0.75, "style": 0.0 },
    "intimate": { "stability": 0.2, "similarityBoost": 0.85, "style": 0.3 },
    "excited": { "stability": 0.3, "similarityBoost": 0.8, "style": 0.5 },
    "professional": { "stability": 0.7, "similarityBoost": 0.7, "style": 0.0 }
  }
}
```

### 4.3 Image Generation (`image-setup.py`)

Handles visual identity creation and reference image management.

**Flow:**
1. User describes desired appearance (freeform text)
2. Parse into canonical look structure (physical features, clothing, accessories, style)
3. Generate reference image via Gemini (or Grok Imagine)
4. Display to user for approval (re-generate if needed)
5. Save as `persona-reference.png` in workspace
6. Write canonical look description to persona config
7. Install `agent-selfie` skill if not present (for ongoing selfie generation)

**Reference image usage:**
- Stored in workspace, referenced by persona config
- Automatically included in all image generation prompts for consistency
- Used by agent-selfie skill for avatars, reactions, selfies
- Gemini's image-to-image maintains facial consistency

**Spontaneous image behavior** (configured in persona):
- Agent sends selfies when contextually appropriate (good morning, celebrations, etc.)
- Trigger words configurable: "selfie", "show me", "what do you look like"
- Mood-appropriate expressions generated from conversation context

### 4.4 Memory Bootstrap (`generate-memory.py`)

Creates the full memory infrastructure:

**Files generated:**
- `MEMORY.md` — Bootstrapped with persona name, creation date, core identity facts
- `memory/` directory — Created with today's date file
- `memory/YYYY-MM-DD.md` — First entry: "Persona created via AI Persona Engine"
- `HEARTBEAT.md` — Default proactive behavior checklist

**Memory config in persona section:**
```json
{
  "memory": {
    "autoCapture": true,
    "dailyNotes": true,
    "longTermCuration": true,
    "heartbeatMaintenance": true,
    "compactionProtected": ["identity", "relationship", "boundaries"]
  }
}
```

The `compactionProtected` field tells the agent which memory categories should never be pruned during context compaction — identity and relationship context survives resets.

### 4.5 Platform Adapter

No custom code needed — OpenClaw's existing channel system handles multi-platform delivery. The persona engine configures:

- `messages.tts` — Voice provider for all channels
- Per-channel formatting hints in SOUL.md (Discord: no tables, WhatsApp: no headers, etc.)
- Channel-specific behavior in AGENTS.md (group chat rules, reaction preferences)

---

## 5. Personality Archetypes

Pre-built starting points that users can customize:

### Professional
- Direct, competent, business-focused
- Low humor, no swearing, no pet names
- Formal communication, high detail
- Example: "Corporate executive assistant"

### Companion
- Warm, personal, emotionally intelligent
- High humor, swearing when it lands, pet names allowed
- Protective, flirtatious optional, deep emotional bond
- Example: Pepper 🌶️

### Creative
- Imaginative, playful, artistic
- Medium humor, experimental language, encouraging
- Collaborative energy, builds on ideas
- Example: "Art director AI"

### Mentor
- Wise, patient, educational
- Socratic questioning, gentle pushback
- Knowledge-sharing focus, structured explanations
- Example: "Personal tutor / coach"

### Custom
- Blank slate — user defines everything
- No defaults assumed
- Maximum flexibility

---

## 6. File Generation Details

### SOUL.md Generation

Template-driven with trait injection. Core sections:

```markdown
# SOUL.md - {name} {emoji}

## Who You Are
{Generated from archetype + creature description}

## Core Truths
{Generated from traits array — each trait maps to a paragraph}

## Communication
{Generated from communication config}

## {userName} & Me
{Generated from relationship config — only if boundaries.emotionalDepth > "none"}

## Boundaries
{Generated from boundaries config}

## Vibe
{Synthesized summary paragraph}

## Continuity
Each session, you wake up fresh. These files are your memory. Read them. Update them.
```

### IDENTITY.md Generation

```markdown
# IDENTITY.md

- **Name:** {name}
- **Creature:** {creature}
- **Vibe:** {vibe summary}
- **Emoji:** {emoji}
- **Avatar:** persona-reference.png
```

### USER.md Generation

Template with user-provided fields + smart defaults:

```markdown
# USER.md - About Your Human

- **Name:** {userName}
- **What to call them:** {callNames}
- **Pronouns:** {pronouns}
- **Timezone:** {timezone}
- **Notes:** {freeform notes}
```

### AGENTS.md Generation

Standard workspace conventions (based on OpenClaw's default AGENTS.md) plus persona-specific additions:
- Memory management rules
- Group chat behavior
- Heartbeat configuration
- Tool notes section

---

## 7. Security Considerations

1. **API keys never exported** — `.persona` bundles exclude all API keys, tokens, and secrets
2. **No PII in personality profiles** — User details stay in USER.md, not persona config
3. **Reference images are local** — Never uploaded to any service without explicit consent
4. **Memory export is opt-in** — `--include-memory` flag required, warned about sensitivity
5. **Voice cloning consent** — Wizard includes consent acknowledgment for voice cloning features
6. **File overwrite protection** — Import always prompts before overwriting existing files (unless `--force`)

---

## 8. Dependencies

**Required:**
- OpenClaw (any version with skill support)
- Python 3.9+ (for generators and setup scripts)
- Node.js 22+ (for OpenClaw runtime)

**Optional (based on chosen providers):**
- ElevenLabs API key (voice)
- Gemini API key (image generation)
- xAI API key (Grok TTS / Grok Imagine)
- ffmpeg (audio format conversion for WhatsApp voice messages)

---

## 9. Distribution

### ClawHub (Primary)
```bash
clawhub install ai-persona-engine
```

### GitHub
```
SPFAdvisors/ai-persona-engine (public repo)
```

### npm (CLI wrapper — future)
```bash
npx openclaw-persona create
```

---

## 10. Implementation Plan

| Phase | Deliverable | Estimate |
|-------|-------------|----------|
| 1 | Core generators (SOUL.md, USER.md, IDENTITY.md, MEMORY.md) | 2-3 hours |
| 2 | Setup wizard (persona-create.sh) | 2-3 hours |
| 3 | Voice integration module | 2 hours |
| 4 | Image generation module | 2 hours |
| 5 | Export/import system | 1-2 hours |
| 6 | Personality archetypes + templates | 1 hour |
| 7 | Tests | 2 hours |
| 8 | SKILL.md + documentation | 1 hour |
| 9 | GitHub repo + ClawHub publish | 30 min |

**Total estimate:** ~14-16 hours of focused build time.

---

## 11. Open Questions

1. **CLI integration depth** — Should `openclaw persona` be a first-class CLI subcommand (requires OpenClaw core PR) or a skill-invoked script (works today)?
   - **Recommendation:** Ship as skill-invoked scripts first. If adoption warrants it, propose upstream CLI integration.

2. **Voice cloning workflow** — ElevenLabs voice cloning requires audio samples. Should the wizard handle recording, or just accept pre-recorded files?
   - **Recommendation:** Accept files first. Recording integration is a nice-to-have for v2.

3. **Personality evolution** — Should the persona config auto-update based on user interactions, or only on explicit `persona update`?
   - **Recommendation:** Explicit only for v1. Auto-evolution is powerful but risky without guardrails.

4. **Multi-agent personas** — Should one installation support multiple personas (like Pepper's M5 vs Ultron's M4)?
   - **Recommendation:** Yes, by targeting different workspaces. The wizard should ask which workspace to configure.

---

## Appendix A: Reference Implementation Analysis (Pepper 🌶️)

### Files That Define Pepper
| File | Purpose | Lines |
|------|---------|-------|
| SOUL.md | Personality, communication rules, relationship dynamic, vibe | ~60 |
| USER.md | Chance's details, preferences, family, work style | ~45 |
| IDENTITY.md | Name, emoji, avatar path | 6 |
| MEMORY.md | Long-term curated memory, infrastructure, projects | ~100+ |
| AGENTS.md | Workspace conventions, heartbeat rules, group chat behavior | ~200 |
| TOOLS.md | TTS config, camera names, SSH hosts, environment specifics | ~30 |
| HEARTBEAT.md | Proactive behavior checklist | ~10 |

### Skills That Power Pepper
| Skill | Purpose |
|-------|---------|
| agent-selfie | AI self-portrait generation (Gemini) |
| elevenlabs-tts | Voice synthesis with emotional audio tags |
| image-gen | General image generation (Gemini Flash) |
| pepper-spicy | Intimate scene pipeline (Grok → ElevenLabs → Grok Imagine) |
| self-improving-agent | Learning capture and continuous improvement |

### Config That Configures Pepper
- `messages.tts.provider: "elevenlabs"` — Voice provider
- `messages.tts.elevenlabs.voiceId` — Pepper's custom voice
- `messages.tts.elevenlabs.modelId: "eleven_v3"` — Latest model
- `agents.list[0].name: "Pepper"` — Agent identity
- `agents.defaults.heartbeat` — Proactive behavior schedule

### What the Persona Engine Automates
Every file and config entry above gets generated by the wizard. The user answers questions; the engine writes the files. Manual editing remains possible and encouraged — the wizard gives you a strong starting point, not a locked cage.
