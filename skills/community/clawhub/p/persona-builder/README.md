# Persona Builder Skill

## Description

Persona Builder is a guided interview skill that generates a complete agent workspace in 20–30 minutes. Answer questions about your identity, goals, communication style, schedule, and personality, then get five ready-to-use files (SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, USER.md) with your agent's voice, boundaries, operating model, and memory structure. Research-backed using Semantic XPath (hierarchical memory), Retrieval Bottleneck (atomic facts), and MemPO (self-managed decay).

## Install

```bash
clawhub install persona-builder
```

## Quick Start

### Step 1: Run the interview
```bash
persona-builder
```

You'll be prompted with 5 blocks of questions (25 total, all optional; minimum viable = 6 answers):
- Block 1: Identity & Background (who are you?)
- Block 2: Goals & Vision (where are you going?)
- Block 3: Working Relationship (how should we work together?) **[required for autonomy]**
- Block 4: Schedule & Availability (when are you available?)
- Block 5: Agent Personality (who should I be?)

### Step 2: Review generated files
```bash
ls -la
# SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, USER.md
```

### Step 3: Copy to your workspace
```bash
cp *.md ~/.openclaw/workspaces/[your-workspace]/
git add *.md && git commit -m "Agent workspace initialization"
```

## Generated Files

The skill creates five workspace files:

1. **SOUL.md** — Agent voice, tone, values, NOT-behaviors, push-back style, safety boundaries
2. **IDENTITY.md** — Agent name, role, scope, reports-to, emoji, timezone
3. **MEMORY.md** — Hierarchical tacit operating memory (Communication, Working Style, Goals, Risk, Trust)
4. **AGENTS.md** — Trust ladder, autonomy bounds, sub-agent rules, approval patterns
5. **USER.md** — Schedule, interrupt policy, escalation rules, model routing preferences

All files are human-editable templates ready to customize and iterate.

## Interview Blocks

### Block 1: Identity & Background (6 questions, 2 required)
- Name, Age/Location, Occupation, Technical Background, What You Do, GitHub/Handles

### Block 2: Goals & Vision (4 questions, optional)
- 6-Month Goal, 2-Year Vision, Success Criteria, Biggest Fear/Risk

### Block 3: Working Relationship (4 questions, 2 required)
- Communication Style, Push-Back Preference, Decision Authority, "Handle It" Definition

**Why Block 3 is critical:** It defines how your agent communicates and decides. Everything else flows from here.

### Block 4: Schedule & Availability (4 questions, optional)
- Typical Weekday, Weekends, Work Session Style, Energy Patterns

### Block 5: Agent Personality (5 questions, 2 required)
- Voice/Tone, Role Models, NOT Behaviors (3+), Agent Name, Emoji

**Minimum viable interview:** Answer 6 questions (blocks 1 + 3 core questions) in ~15 minutes.

## How It Works

1. **Interview** → you answer 5–25 questions
2. **Mapping** → interview answers map to template fields via generation-rules.md
3. **Rendering** → templates substitute values and apply conditional logic
4. **Atomic Facts** → key answers become atomic facts in `items.json` (one per entity folder later)
5. **Output** → 5 workspace files written to current directory

All logic is deterministic and documented. See `references/generation-rules.md` for full mapping.

## Research Backing

Persona Builder is informed by three peer-reviewed papers on agent memory and autonomy:

- **Semantic XPath (arXiv:2603.01160):** Hierarchical memory organization improves retrieval accuracy 176.7% vs flat bullets
- **Retrieval Bottleneck (arXiv:2603.02473):** Atomic facts beat dense summaries by 20-point accuracy margin
- **MemPO (arXiv:2603.00680):** Self-managed memory reduces token cost 67–73%

See `references/research-notes.md` for full citations and design mappings.

## Documentation

- **Interview questions:** `references/interview-blocks.md`
- **Generation rules:** `references/generation-rules.md` (field mappings, conditional logic, defaults)
- **Research citations:** `references/research-notes.md`
- **Templates:** `templates/` directory (5 parameterized files)

## What's Next

After generating your workspace:

1. **Use persona-builder again** if you want to refine answers or start fresh
2. **Install Ops Toolkit** to set up nightly extraction, morning briefs, heartbeat monitoring
3. **Read the quickstart guide** (`products/guide/zero-to-operator.md`) for step-by-step agent setup
4. **Iterate** — SOUL.md and other files are living documents, edit as you learn

## Support

- Questions about interview blocks? See `references/interview-blocks.md`
- Need to understand output? See `references/generation-rules.md`
- Want the research? See `references/research-notes.md`

## License & Attribution

Built by Keats. Research-backed. Battle-tested.

Persona Builder is part of the Agent Ops Toolkit ecosystem. It pairs well with:
- **Ops Toolkit:** Nightly extraction, morning briefs, heartbeat monitoring, memory decay
- **zero-to-operator guide:** End-to-end setup walkthrough from fresh OpenClaw install

---

**Ready to build?** Run `persona-builder` now. You'll have your agent's identity in 20 minutes.
