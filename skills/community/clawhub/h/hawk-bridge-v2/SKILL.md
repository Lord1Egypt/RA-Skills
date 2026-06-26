# Auto-Evolve v4.4 (build 57fe0d7)

**Four-perspective automated inspection and iteration manager.**

> Make your projects continuously better — automatically.

---

## Core Philosophy

**auto-evolve is not just a code scanner — it's a巡检伙伴 that thinks like a human.**

On each scan, auto-evolve simulates receiving a Feishu message:

> "What else can this project improve? Any shortcomings?"

It then examines the project from four perspectives, forming real opinions — not mechanically listing issues.

---

## Scan Workflow (v4.0)

```
auto-evolve scan
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  Step 1: project-standard project type detection      │
│  Detects: Skill / CLI / Python Library / Web / ...  │
│  Determines perspective weights + inspection focus     │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│  Step 2: Four-perspective inspection               │
│                                                      │
│  👤 USER    → user/user-perspective.md (criteria) │
│  📦 PRODUCT → product-requirements.md (criteria)  │
│  🏗 PROJECT → project-inspection.md (criteria)     │
│  ⚙️ TECH   → code-standards.md (criteria)       │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│  Step 3: project-standard reference docs            │
│  Used as evaluation criteria, output grouped report  │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│  Step 4: Execute / Notify / Record to learnings    │
└─────────────────────────────────────────────────────┘
```

### Relationship with project-standard

| Component | Role |
|----------|------|
| **project-standard** | Defines taxonomy + four-perspective framework + reference docs (judging criteria) |
| **auto-evolve** | Loads standards, runs inspection, records learnings, executes improvements |

---

## Four-Perspective Framework

```
┌─────────────────────────────────────────────────────┐
│              auto-evolve Inspection Framework v4.0    │
├──────────────┬──────────────────┬───────────────────┤
│   User      │     Product      │     Project       │    Tech        │
│  "Usable?"  │ "Delivered?"    │   "Healthy?"     │  "Clean?"      │
├──────────────┼──────────────────┼───────────────────┼──────────────────┤
│ CLI design  │ Feature complete │ Learnings closed  │ Code quality   │
│ Learning    │ Promise kept     │ Scan history     │ Architecture  │
│ Errors      │ Pain resolved   │ Config rational  │ Test coverage  │
│ Fault tol.  │ Docs match code │ Dependency health│ Performance   │
└──────────────┴──────────────────┴───────────────────┴──────────────────┘
```

---

## Four Perspectives Detail

### 👤 User Perspective

**Core question: Is it pleasant to use?**

| Ask | Finds |
|-----|-------|
| CLI design | Non-intuitive flags, missing defaults |
| Learning curve | How long for a newcomer? |
| Error messages | Machine-speak vs human-speak |
| Fault tolerance | What on partial failure? |
| Workflow | Steps per operation? |

### 📦 Product Perspective

**Core question: Does it deliver what it promises?**

| Ask | Finds |
|-----|-------|
| README promises | Features claimed but not built |
| Pain points | ❌-marked issues still broken |
| Feature completeness | Half-baked features |
| Docs consistency | Docs ≠ code |

### 🏗 Project Perspective

**Core question: Is it managed well?**

| Ask | Finds |
|-----|-------|
| Learnings loop | Previous findings tracked? |
| Scan rhythm | Regular schedule? |
| Config rationality | Over/under-configured? |
| Dependency health | Outdated deps? Known CVEs? |

### ⚙️ Tech Perspective

**Core question: Is the code healthy?**

| Ask | Finds |
|-----|-------|
| Code quality | Duplicates, long functions |
| Architecture | Module coupling |
| Test coverage | Core logic tested? |
| Performance/security | Bottlenecks, vulnerabilities |

**Note**: Tech is the lowest priority — it's important but should not overshadow product truth.

---

## Scan Output Format

```
🔍 auto-evolve Inspection Report — soul-force
Generated: 2026-04-05 22:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 User Perspective ★★★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 🚨 Impact 0.7
     review command lacks --dry-run, users think it's safe but it writes files
     → Suggestion: Add --dry-run support to review

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Product Perspective ★★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 🚨 Impact 0.8
     README promises "LLM fallback" but code has no fallback
     API failure = tool failure
     → Suggestion: Implement keyword-based rule engine as fallback

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ Tech Perspective ★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [opt] 🟡 duplicate_code: SoulForgeConfig init repeated 15 times
```

---

## Commands

### scan

```bash
# Scan all configured repos
python3 auto-evolve.py scan

# Single repo scan
python3 auto-evolve.py scan --repo /path/to/repo

# Preview mode (no execution)
python3 auto-evolve.py scan --dry-run

# With specific persona memory
python3 auto-evolve.py scan --recall-persona master
```

### confirm / reject / approve

```bash
python3 auto-evolve.py confirm
python3 auto-evolve.py reject 2 --reason "too risky"
python3 auto-evolve.py approve 1,3
```

### repo-add / repo-list

```bash
python3 auto-evolve.py repo-add ~/.openclaw/workspace/skills/hawk-bridge --type skill
python3 auto-evolve.py repo-list
```

### schedule

```bash
python3 auto-evolve.py schedule --every 168
python3 auto-evolve.py schedule --suggest
```

### learnings

```bash
python3 auto-evolve.py learnings
python3 auto-evolve.py learnings --type rejections
python3 auto-evolve.py learnings --summary   # v4.3: summary view
```

### trends (v4.3)

```bash
python3 auto-evolve.py trends --repo soul-force  # Scan trend for a project
python3 auto-evolve.py trends --all              # All projects
```

---

## Configuration

`~/.auto-evolverc.json`

```json
{
  "mode": "semi-auto",
  "full_auto_rules": {
    "execute_low_risk": true,
    "execute_medium_risk": false,
    "execute_high_risk": false
  },
  "schedule_interval_hours": 168,
  "repositories": [
    {
      "path": "/path/to/repo",
      "type": "skill",
      "visibility": "public",
      "auto_monitor": true
    }
  ]
}
```

---

## LLM Integration

auto-evolve uses OpenClaw-configured LLM (no separate API key needed).

Priority: `OPENAI_API_KEY` / `MINIMAX_API_KEY` env vars, or `openclaw config get llm`.

---

## Iteration Storage

```
.auto-evolve/
  .iterations/
    {id}/
      manifest.json        -- metadata + findings
      plan.md             -- execution plan
      pending-review.json -- items pending review
      report.md           -- execution report
      metrics.json        -- iteration metrics
  .learnings/
    approvals.json       -- approved changes
    rejections.json      -- rejected changes + reasons
```
