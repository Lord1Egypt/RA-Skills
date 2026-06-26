# LoomLens Live — OpenClaw Skill

**Skill Name:** `loomlens-live`  
**Command:** `/loomlens`  
**Type:** OpenClaw AgentSkill (sidebar panel skill)  
**Phase:** Ready to install  

---

## What It Does

Opens the **LoomLens Live sidebar panel** inside OpenClaw. The panel shows real-time cost estimates for the current prompt across optimized model clusters, recommends the best model within each cluster, and lets you dispatch to any model with one click.

---

## Features

- **6 model clusters** — Flash Reasoning, Fast General, Balanced Coding, Power, Vision
- **Within-group optimization** — recommends cheapest model that clears the capability bar
- **Per-call billing** — type freely for free; only "Run Estimate" deducts from Signal Loom account
- **3 free runs/day** — local preview is unlimited; runs against your Signal Loom key
- **Drag & drop** — drop any text into the sidebar to estimate
- **Keyboard shortcut** — `Cmd/Ctrl+L` to open from anywhere
- **Model dispatch** — select any model and it overrides the next prompt's model via `before_model_resolve` hook
- **Rev-share ready** — developers earn 23–28% revenue share on estimate calls

---

## Billing Model

| Action | Cost |
|--------|------|
| Type a prompt (local preview) | Free — no API call |
| "Run Estimate" (no API key) | Prompts to connect key |
| "Run Estimate" (API key connected) | Per-call billing — deducts from Signal Loom quota |
| Rev-share payout | 23% (Loom Partner) / 28% (Loom Elite) on net estimate revenue |

---

## Freemium

| Tier | Limits | Auth |
|------|--------|------|
| Free | 3 runs / 24h (local preview unlimited) | None |
| API Key | Unlimited runs | Signal Loom API key |

---

## Rev-Share: Loom Partners Program

| Tier | Rate | Qualification |
|------|------|--------------|
| Loom Partner | 23% | 10K mins/month minimum |
| Loom Elite | 28% | 100K mins/month or signed agreement |

See `REV_SHARE_ANALYSIS.md` in the Signal Loom API workspace for full margin and payout analysis.

---

## Model Clusters

| Cluster | Models | Best For |
|---------|--------|----------|
| **Flash Reasoning** | MiniMax M2, Gemini 2.5 Flash, Claude Haiku, DeepSeek v3 | Q&A, summaries, simple tasks |
| **Fast General** | GPT-4o Mini, Gemini 2.0 Flash, xAI Grok-3 | Fast general purpose |
| **Balanced Coding** | Claude Sonnet 4, GPT-4o, Claude 3.5 Sonnet | Medium-complexity code |
| **Power / Architecture** | Claude Opus 4, Claude Code | Complex builds, architecture |
| **Vision / Multimodal** | GPT-4o, Claude 3.5 | Images, PDFs, documents |

---

## Scoring

```
score = (capability_fit × 0.35) + (cost_efficiency × 0.35) + (speed × 0.30)
```

Within each cluster: cheapest model that scores ≥65 gets the **💡 Best in group** badge.

---

## Installation

### Option A: Workspace Hook (Quick)

```bash
cp -r signal-loom-loomlens/ ~/.openclaw/workspace/hooks/loomlens-live/
```

### Option B: OpenClaw Skill Install (When supported)

```bash
openclaw skills install ./signal-loom-loomlens
```

---

## Files

```
signal-loom-loomlens/
├── SKILL.md                      — This file
├── loomlens-sidebar.html         — Self-contained sidebar panel (deploy anywhere)
├── loomlens-engine.js           — Estimation engine (pure JS, no dependencies)
├── loomlens-clusters.js         — Cluster definitions + scoring
├── loomlens-openclaw-plugin.ts  — Plugin with before_model_resolve hook
└── dist/                        — Pre-built deploy artifacts
```

---

## Branding

- **Attribution:** "Powered by Signal Loom AI ✦" in sidebar footer
- **External link:** "Get a Signal Loom API key →" → signallloomai.com/signup.html
