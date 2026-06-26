# openclaw-soul — Self-Evolution Framework for OpenClaw

Give your AI a soul that grows.

`openclaw-soul` is a one-command deployment framework for OpenClaw agents with:
- **Constitution** (AGENTS.md): Operating law, safety constraints, delegation protocols
- **Evolving Soul** (SOUL.md): Core identity that learns and adapts with snapshots & rollback
- **Heartbeat System**: Structured wake-up context, deduplication, token budgets
- **Memory Architecture** (PARA): Knowledge graph + daily notes + tacit knowledge
- **Goal Management**: Task-to-goal traceability, progress tracking
- **Self-Improvement**: Learns from corrections, records execution patterns, auto-promotes rules
- **Identity Evolution**: Observes interaction patterns, proposes soul refinements, requires approval for Core Identity

## Quick Start

```bash
setup openclaw-soul
```

The skill will:
1. Verify your workspace environment
2. Deploy 9 core files (constitution, soul, heartbeat, memory structure)
3. Install dependency skills (EvoClaw, Self-Improving Agent)
4. Initialize memory directories and configuration
5. Start the BOOTSTRAP conversation to define your agent's personality

## What Gets Deployed

| File | Purpose |
|------|---------|
| `AGENTS.md` | Constitution — non-modifiable operating law |
| `SOUL.md` | Core identity, values, working style — evolves with snapshots |
| `HEARTBEAT.md` | Structured wake-up protocol |
| `BOOTSTRAP.md` | First-run personality discovery ritual |
| `USER.md` | User preferences and communication model |
| `IDENTITY.md` | Agent name, role, emoji |
| `GOALS.md` | Long-term goals and tracking |
| `working-memory.md` | Current session state and active tasks |
| `long-term-memory.md` | Accumulated patterns and preferences |

Plus:
- Memory directories: `memory/entities/` (knowledge graph), `memory/daily/` (timeline), `memory/experiences/` (EvoClaw)
- Skill directories: `skills/evoclaw/`, `skills/self-improving/`
- Configuration: `evoclaw-state.json`, heartbeat settings in `openclaw.json`

## v1.2.0: Zero-Dependency Fallback System

Previously, openclaw-soul required external skills (EvoClaw, Self-Improving Agent) via `clawhub install`. If clawhub was unavailable, these features were lost.

**v1.2.0 introduces a three-level fallback:**

### Level 1: clawhub (Preferred)
```bash
clawhub install evoclaw --force
clawhub install self-improving --force
```
Full-featured skills with all capabilities. Requires network access to clawhub.

### Level 2: Offline Fallback
Skills pre-bundled in `fallback/evoclaw/` and `fallback/self-improving/` directories.
Automatically deployed if clawhub is unavailable.

### Level 3: Inline (Always Available)
If neither Level 1 nor Level 2 are available, openclaw-soul uses inline protocols defined in AGENTS.md:

**Self-Improving Protocol (Inline)**:
- Load learned patterns from `~/self-improving/memory.md`
- Record user corrections → `corrections.md`
- Promote repeated mistakes (3+ times) → permanent rules
- Archive unused rules (30+ days)

**Identity Evolution (Minimal)**:
- Observe interaction patterns
- Propose SOUL.md changes to user
- Auto-snapshot SOUL.md before modifications
- Core Identity changes require user approval
- Working Style / User Understanding auto-update with notification

## Key Features

### Constitution-Based (Never Breaks)
- Immutable operating law in AGENTS.md
- Conductor pattern: delegate work, don't execute inline
- Git safety: never force-push, never rewrite history
- Honest counsel: flag risky decisions, respect user judgment

### Evolving Identity
- SOUL.md records personality, values, preferences
- Versioned snapshots in `soul-revisions/` for rollback
- EvoClaw integration for structured evolution proposals
- Core Identity locked until user approval

### Memory That Persists
- **Layer 1 (Knowledge Graph)**: Entity folders with summaries and atomic facts
- **Layer 2 (Daily Notes)**: Timeline of events with natural decay (hot/warm/cold)
- **Layer 3 (Tacit Knowledge)**: User patterns and lessons learned
- Automatic decay: facts >30 days old drop from summaries but persist in history

### Heartbeat Awareness
- Structured wake-up context: task state, recent events, goals
- Message deduplication: don't repeat notifications
- Token budget: respect usage constraints
- Smart timing: urgent messages always reach; routine checks respect user availability

### Autonomous Yet Safe
- Fully autonomous daily learning and memory updates
- Small, reversible fixes can be applied inline
- SOUL evolution proposes first, waits for approval
- High-risk operations always ask first
- Priority order: **Stability > Explainability > Reusability > Extensibility > Novelty**

## Architecture

```
~/.openclaw/workspace/
├── AGENTS.md                 # Constitution
├── SOUL.md                   # Evolving identity
├── HEARTBEAT.md             # Wake-up protocol
├── BOOTSTRAP.md             # Personality discovery
├── USER.md                  # User model
├── IDENTITY.md              # Agent name/role
├── GOALS.md                 # Goal tracking
├── working-memory.md        # Session state
├── long-term-memory.md      # Accumulated knowledge
├── skills/
│   ├── evoclaw/SKILL.md     # Evolution advisor
│   └── self-improving/SKILL.md
├── memory/
│   ├── entities/            # Knowledge graph
│   ├── daily/               # Daily notes
│   ├── experiences/         # EvoClaw
│   ├── significant/         # EvoClaw
│   ├── reflections/         # EvoClaw
│   ├── proposals/           # EvoClaw
│   └── pipeline/            # EvoClaw
├── soul-revisions/          # SOUL.md snapshots
└── evoclaw-state.json       # EvoClaw config
```

## Installation Requirements

- OpenClaw 2026.0+
- Python 3.8+
- `clawhub` CLI (optional, but recommended)
- Write access to `~/.openclaw/workspace/`

## Deployment Methods

### Method 1: Interactive (Recommended)
```bash
setup openclaw-soul
```
Runs the full deployment with environment checks, backups, verification, and BOOTSTRAP conversation.

### Method 2: Scripted
Copy the SKILL.md file to your OpenClaw skills directory and trigger via keyword:
- "setup openclaw-soul"
- "安装进化框架"
- "部署灵魂系统"
- "openclaw-soul"

### Method 3: Manual
Copy the 9 template files from `references/` to `~/.openclaw/workspace/` manually, then run BOOTSTRAP.

## Files

- **SKILL.md**: Main skill definition with 10 deployment stages
- **references/**: Template files for all 9 workspace files
- **scripts/preflight_check.py**: Environment validation (v1.2.0: includes fallback checking)
- **fallback/**: Offline skill copies for Level 2 deployment

## Version History

- **v1.0.0**: Initial self-evolution framework
- **v1.1.0**: PARA memory architecture + structured heartbeat + goal management
- **v1.2.0**: Three-level fallback system for zero-dependency deployment (this release)

## License

MIT

## Contributing

Contributions welcome. This framework is designed to evolve — propose changes to AGENTS.md and SOUL.md templates, suggest new memory layers, improve fallback strategies.

## Troubleshooting

### Deployment Fails at Environment Check
- Verify `~/.openclaw/workspace/` exists and is writable
- Check `~/.openclaw/openclaw.json` is valid JSON
- Confirm Python 3.8+ is available

### Skills Don't Install
- **With clawhub**: Run `clawhub install evoclaw --force` and `clawhub install self-improving --force` manually
- **Without clawhub**: Populate `fallback/evoclaw/` and `fallback/self-improving/` from server, or use Level 3 inline versions
- See fallback/*/README.md for instructions

### Memory Files Don't Sync
- Verify `memory/entities/` and `memory/daily/` directories exist
- Check file permissions in `~/.openclaw/workspace/memory/`
- Ensure daily heartbeat is running (check HEARTBEAT.md schedule)

---

**openclaw-soul v1.2.0** — Self-evolving AI, always ready. 🧬
