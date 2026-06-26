<div align="center">

# 🧭 Identity Compass

### You already know what you want. You just can't see it yet.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://python.org)

[English](#the-problem) · [한국어](README_KO.md) · [中文](README_ZH.md)

<br>
<img src="assets/compass-demo.jpg" alt="Identity Compass Demo" width="600">
<br><br>
<img src="assets/slide-01.png" alt="Life Compass AI" width="500">

</div>

---

## The Problem

You've taken personality tests. Set goals on January 1st. Made pros-and-cons lists. And still — when it actually matters — you freeze.

**"Should I take this job?"**
**"Is this relationship right for me?"**
**"Am I heading in the right direction?"**

The real answer is already inside you. It's scattered across hundreds of small decisions you've already made — what excited you, what drained you, what you kept coming back to, what you quietly avoided.

**No one is tracking those patterns. Until now.**

## What Identity Compass Does

It watches your conversations. Not to judge — to **listen**.

Every time you express a preference, reject something, light up about an idea, or hesitate at a crossroads — the system captures it as a tiny compass needle. Over time, those needles align. A direction emerges.

Then, when you face a real decision, instead of guessing, you can ask:

> *"Does this choice point the same way I've been pointing all along?"*

### Real Examples

| You say... | The system sees... |
|-----------|-------------------|
| "I'd rather build my own thing than follow someone else's playbook" | Strong autonomy signal |
| "That job pays well but I'd just be executing" | Anti-pattern: execution without ownership |
| "I lost track of time working on that side project" | Flow state → core value indicator |
| "Honestly, I'm jealous of how she lives" | Aspiration signal → direction candidate |

You don't fill out forms. You don't answer questionnaires. You just... talk. The compass does the rest.

<div align="center">
<img src="assets/slide-02.png" alt="Are we heading in the right direction?" width="500">
<br><em>Are your countless choices actually leading you toward your true goals?</em>
<br><br>
<img src="assets/slide-03.png" alt="Decision marbles in 3D space" width="500">
<br><em>Every decision is a marble with a direction vector — small ones for coffee, big ones for career moves.</em>
</div>

## What You Get

### 🎯 Your Direction (H Vector)
A one-liner that captures who you are — not who you think you should be.

> *"Chooses autonomy over structure, builds depth through research, drives innovation over comfort."*

This isn't a horoscope. It's computed from your actual decisions.

### 📊 Your Alignment Score (M)
A single number (0 to 1) showing how aligned your recent choices are with your true direction.

- **0.8+** → You're locked in. Decisions are coherent.
- **0.5-0.7** → Mostly on track, some noise.
- **Below 0.3** → You're pulling in multiple directions. Time to reflect.

### ⚖️ Decision Simulation
Facing a fork in the road? Each option gets simulated:

```
Option A: Take the startup offer
  → Alignment shifts from 0.68 → 0.72 ✅

Option B: Stay at current job  
  → Alignment shifts from 0.68 → 0.61 ⚠️
```

Not "Option A is better." Instead: **"Option A is more *you*."**

<div align="center">
<img src="assets/slide-06.png" alt="Decision simulation" width="500">
<br><em>Simulate decisions before you make them.</em>
</div>

### 🗺️ Your Decision Map
An interactive visualization where every past decision is a marble — sized by importance, colored by alignment. Watch your patterns emerge in real time.

## Who This Is For

- **Career changers** — "I know I need to leave, but where do I go?"
- **Founders** — "Am I building what I actually care about?"
- **Anyone at a crossroads** — "This feels right but I can't explain why"
- **People tired of generic advice** — This is built from *your* data, not a template

## What This Is NOT

- ❌ Not a personality test (no self-reporting)
- ❌ Not a goal-setting app (goals change; direction persists)
- ❌ Not an AI that decides for you (data, not decisions)
- ❌ Not cloud-based (everything stays on your machine)

<div align="center">
<img src="assets/slide-07.png" alt="Standard AI vs Compass AI" width="500">
<br><em>Generic AI gives you facts. Compass AI gives you alignment.</em>
</div>

## Quick Start

### 1. Install the skill

```bash
# Option A: via ClawHub (recommended)
npx clawhub@latest install identity-compass

# Option B: manual
git clone https://github.com/ico1036/identity-compass.git
cp -r identity-compass/ ~/.openclaw/workspace/skills/identity-compass/
```

### 2. Set up your Obsidian vault

The compass stores your decision vectors in an [Obsidian](https://obsidian.md)-compatible vault. Create this structure:

```
~/.openclaw/workspace/obsidian-vault/compass/
├── vectors/          # Individual decision notes (auto-created by agent)
│   ├── career-change-decision.md
│   ├── rejected-offer-at-bigcorp.md
│   └── ...
├── clusters/         # Grouped patterns (auto-created)
│   ├── autonomy-first.md
│   └── depth-builder.md
├── signals/          # Raw conversation signals (auto-created)
│   └── 2026-03.md
└── prior/            # Phase 1 dialectical results (auto-created)
    └── h-vector.md
```

You just need to create the root folders — the agent fills them:

```bash
mkdir -p ~/.openclaw/workspace/obsidian-vault/compass/{vectors,clusters,signals,prior}
```

### 3. Start talking

That's it. Talk to your [OpenClaw](https://openclaw.ai) agent normally. The compass activates automatically when it detects decision signals:

- Career discussions, job comparisons
- "Should I do A or B?"
- Preferences, rejections, excitement
- Life direction questions

The agent extracts vectors silently in the background. No forms, no questionnaires.

### 4. See your map

```bash
cd ~/.openclaw/workspace/skills/identity-compass/scripts
python3 -m http.server 8742
# Open http://localhost:8742/visualize_2d.html
```

The visualization loads from `compass_data.json` (auto-generated by the agent). If you want to manually inspect or edit your data, see below.

---

## Data Files

The compass uses JSON files in `scripts/` — all auto-managed by the agent, but you can inspect or edit them:

| File | Purpose | Auto-generated? |
|------|---------|:---:|
| `compass_data.json` | Visualization data (beads + H + clusters) | ✅ |
| `vectors.json` | Raw decision vectors with metadata | ✅ |
| `magnetization.json` | Computed H direction + M score | ✅ |
| `sample_data.json` | Demo data for first-time setup | Included |

### Creating compass_data.json manually

If you want to customize or bootstrap your visualization before the agent has enough data:

```bash
cp scripts/sample_data.json scripts/compass_data.json
```

Then edit `compass_data.json`:

```json
{
  "identity": [
    {
      "what": "Built my own trading system",
      "why": "Autonomy over following others' playbooks",
      "dir": [0.8, 0.6, 0.7],
      "w": 9,
      "cl": "identity",
      "status": "core"
    }
  ],
  "opportunities": [
    {
      "what": "Company X — Role Y",
      "why": "High autonomy, small team",
      "dir": [0.7, 0.5, 0.8],
      "w": 7,
      "cl": "hot",
      "status": "Applied ✅",
      "match": 0.85
    }
  ],
  "H": {"dir": [0.6, 0.6, 0.6], "mag": 0.70},
  "oneLiner": "Your one-line identity summary",
  "clusters": [
    {"name": "AUTONOMY", "m": 0.75, "color": "#00c8ff"},
    {"name": "DEPTH", "m": 0.70, "color": "#a855f7"},
    {"name": "INNOVATION", "m": 0.80, "color": "#00ff88"}
  ]
}
```

**Field guide:**

| Field | Description |
|-------|-------------|
| `dir` | 3D vector: `[autonomy, depth, innovation]`. Range: -1 to 1 |
| `w` | Weight (1-10). Based on: financial impact, time commitment, irreversibility, emotional intensity |
| `cl` | Color class: `identity`, `hot`, `active`, `warm`, `tension`, `cool`, `avoid` |
| `match` | Cosine similarity with H vector (0-1). Only for opportunities |
| `H.dir` | Your core direction vector (computed from all identity beads) |
| `H.mag` | Magnetization (0-1). How aligned your decisions are |

> **Note:** All personal data files (`compass_data.json`, `vectors.json`, `magnetization.json`) are in `.gitignore` — they never leave your machine.

---

<details>
<summary><b>🔬 How It Works (Technical Details)</b></summary>

### The Physics Model

Identity Compass borrows from **statistical mechanics**. Each decision is a magnetic spin with direction and intensity. The system computes:

- **H (Magnetic Field)** = your core direction, extracted via dialectical dialogue
- **M (Magnetization)** = net alignment of all spin vectors with H
- **Decay** = older decisions fade at `0.95^(days/30)` — who you are *now* matters more

### Three Axes

| Axis | (+) | (−) |
|------|-----|-----|
| X | Autonomy | Structure |
| Y | Depth | Breadth |
| Z | Innovation | Stability |

### Phase 1: Dialectical Extraction

Instead of asking "what do you want?", the system uses four dialogue patterns:
1. **Dilemma** — forced trade-offs reveal hidden priorities
2. **Time-shift** — "what would past-you think of present-you?"
3. **Contradiction** — "you said X but did Y..."
4. **Completion** — "you already know, don't you?"

### Phase 2: Bayesian Vector Collection

Each decision is extracted with:
- 3D direction vector
- Weight (1-10) based on: financial impact, time commitment, irreversibility, emotional intensity, mention frequency
- Beta(α,β) posterior updates per axis

### Phase 3: Virtual Simulation

New choices become virtual marbles → ΔM computed for each option → alignment comparison.

### Architecture

```
identity-compass/
├── SKILL.md                          # Agent protocol
├── references/
│   ├── dialectical-protocol.md       # 7-dimension dialogue system
│   └── bayesian-update.md            # Posterior math
├── scripts/
│   ├── export_vectors.py             # Vault → vectors.json
│   ├── calculate_magnetization.py    # H + M computation
│   └── visualize_2d.html             # 2D marble visualization
└── example-vault/                    # Obsidian template
```

### Data Flow

```
Conversation → Signal Detection → Vector Extraction → Obsidian Vault
    → export_vectors.py → vectors.json → calculate_magnetization.py
    → magnetization.json → visualize_2d.html
```

</details>

---

## Contributing

This is early. The model works, but there's so much to explore:

- [ ] Time-series: watch your direction evolve over months
- [ ] Team compass: what happens when a group computes shared H?
- [ ] Integration with Notion, Logseq, and other note systems
- [ ] More dialogue protocols for different cultures/languages

PRs and ideas welcome.

## License

[MIT](LICENSE)

## Author

**Jiwoong Kim** — [@ico1036](https://github.com/ico1036)

---

<div align="center">

*"The compass doesn't tell you where to go.*
*It shows you where you've been heading all along."*

</div>
