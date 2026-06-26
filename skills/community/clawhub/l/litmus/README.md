# Litmus — Run a Parallel Autonomous ML Research Organization on your OpenClaw instance.

<p align="center">
  <img src="assets/banner.png" alt="Litmus">
</p>

<p align="center">
  <a href="https://github.com/kuberwastaken/litmus/actions/workflows/deploy-site.yml"><img src="https://img.shields.io/github/actions/workflow/status/kuberwastaken/litmus/deploy-site.yml?branch=main&style=for-the-badge" alt="Deploy status"></a>
  <a href="package.json"><img src="https://img.shields.io/badge/version-1.1.1-ff4500?style=for-the-badge" alt="Version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT--0-blue?style=for-the-badge" alt="MIT-0 License"></a>
  <a href="https://clawhub.ai/kuberwastaken/litmus"><img src="https://img.shields.io/badge/OpenClaw-skill-8a2be2?style=for-the-badge" alt="ClawHub skill"></a>
</p>

**Litmus** is an [OpenClaw](https://github.com/openclaw/openclaw) skill that turns your always-on GPU machine into a self-directing ML research lab. Multiple native subagents run experiments overnight, each on their own git branch. A Director steers them every two hours. A Synthesizer distills collective knowledge into a reusable skills library at 04:00. A circadian rhythm shifts agents into creative thinking at 03:00. A research narrative lands in your chat by 08:00.

Built on [Karpathy's autoresearch](https://github.com/karpathy/autoresearch). Everything is a native `sessions_spawn` subagent — no external CLI processes, no PID files.

[Website](https://litmus.kuber.studio) · [Docs](https://litmus.kuber.studio/docs) · [ClawHub](https://clawhub.ai/kuberwastaken/litmus)

Install by asking your OpenClaw agent:
> **"Install https://clawhub.ai/kuberwastaken/litmus and set it up for my machine"**

Your agent checks your GPU, pitches a full schedule (with timing presets), spawns workers, and registers cron jobs — all in one conversation.

---

## What Litmus does that autoresearch doesn't

| Feature | autoresearch | Litmus |
|---|---|---|
| Parallel agents | 1 | 2–8 workers, each on their own git branch |
| Experiment history | Per-run log | Full git tree — every experiment a commit, cherry-pick across agents |
| Cross-agent learning | — | Shared `discoveries.md`, `anomalies.md`, structured `notes/` |
| Knowledge accumulation | — | **Skills library** — validated techniques agents build on, never re-discover |
| Knowledge distillation | — | **Synthesizer** — nightly agent that reads all results and writes reusable skills |
| Active direction | — | Director cron every 2h |
| Stagnation response | — | **Compass Reset** — Director reads skills gap + git history, steers to unexplored combos |
| Dead-end pruning | — | Two-phase budget — 90s quick check before full run, abandon early |
| Structured results | — | JSON attempt record per experiment in `shared/attempts/` |
| Creative thinking | — | Leisure mode 03:00–06:00, paper reading, moonshot hypotheses |
| Paper-grounded ideas | — | arxiv scan → experiment queue |
| Morning briefing | — | Digest to your chat at 08:00 |
| Setup | Manual | Conversational — pitches defaults, asks for changes |

---

## Architecture

```
YOU ──▶ OpenClaw agent
             │
             ├── sessions_spawn ──▶ worker-arch-1 ──┐  each on its own git branch
             ├── sessions_spawn ──▶ worker-opt-2  ──┤  in ~/.litmus/repo/
             ├── sessions_spawn ──▶ worker-gen-3  ──┘
             └── sessions_yield
                                        │
                               ~/.litmus/shared/
                                  attempts/       ← JSON record per experiment
                                  notes/          ← structured YAML-frontmatter notes
                                  skills/         ← validated reusable techniques
                                  discoveries.md
                                  anomalies.md

Director (cron · every 2h during research hours)
  └── reads shared/attempts/ → computes improvement rates
  └── Compass Reset on ≥6 experiments without improvement
  └── cross-pollinates discoveries across agents
  └── assigns anomaly investigation

03:00 ── litmus-leisure   ── arxiv scan · contradiction analysis · writes notes/moonshots/
04:00 ── litmus-synthesizer ── distills notes + attempts → skills/ + research agenda
06:00 ── litmus-dawn      ── reads synthesizer output · queues experiments · wakes workers
08:00 ── litmus-digest    ────────────────────────────────────────────────▶ YOUR CHAT
```

The shared git repo at `~/.litmus/repo/` holds every agent's branch. Browse the full experiment tree any time:
```bash
git -C ~/.litmus/repo log --all --oneline --graph
```

---

## Cron Layer

All times are defaults — configurable during onboarding.

| Job | Default schedule | Role |
|---|---|---|
| `litmus-director` | Every 2h during research hours | Reviews results, Compass Reset on stagnation, cross-pollination |
| `litmus-leisure` | 03:00 daily | Switches workers to thinking mode; reads arxiv; writes structured notes |
| `litmus-synthesizer` | 04:00 daily | Distills notes + attempts into skills library; writes research agenda |
| `litmus-dawn` | 06:00 daily | Reads synthesizer output; queues today's experiments; wakes workers |
| `litmus-watchdog` | Every 30 min | Liveness check, escape mode on zero improvements |
| `litmus-digest` | 08:00 daily | Morning research narrative → delivered to your chat |

---

## Configuration

Onboarding pitches all defaults and asks what you'd like to change. Common presets:

| Preset | Leisure | Synthesizer | Dawn | Digest |
|---|---|---|---|---|
| Standard (default) | 03:00 | 04:00 | 06:00 | 08:00 |
| Night owl | 01:00 | 02:00 | 04:00 | 07:00 |
| Early bird | 23:00 | 00:30 | 02:00 | 05:30 |

Full config options saved to `~/.litmus/config.json`:

| Category | Setting | Default |
|---|---|---|
| Timing | timezone | *ask* |
| Timing | leisure start | 03:00 |
| Timing | synthesizer time | 04:00 |
| Timing | dawn / research resume | 06:00 |
| Timing | digest delivery | 08:00 |
| Timing | director interval | every 2h |
| Timing | watchdog interval | every 30 min |
| Compute | agent count | GPU-based |
| Compute | experiment budget | 300s (5 min) |
| Compute | quick-check budget | 90s (cuts dead ends early) |
| Research | templates | architecture, general |
| Research | custom goal | none |
| Leisure | intensity | standard (3 searches · 5 papers · 5 moonshots) |
| Runtime | mode | subagents *(or claude-code)* |

Defaults in [`configs/default.json`](configs/default.json). Pass custom times to `setup-cron.sh` with `--leisure-start`, `--synthesizer-time`, `--dawn-time`, `--digest-time`, `--director-hours`, `--watchdog-minutes`.

---

## Managing Agents

```bash
# Status — per-agent experiment counts, best val_bpb, stagnation flags, git tree
bash {baseDir}/scripts/status.sh

# Leaderboard — all agents, from shared/attempts/ JSON
bash {baseDir}/scripts/results.sh --top 10
bash {baseDir}/scripts/results.sh --agent arch-1   # single agent

# Full experiment history as a git tree
git -C ~/.litmus/repo log --all --oneline --graph

# Inspect any specific experiment
git -C ~/.litmus/repo show <commit-hash>
cat ~/.litmus/shared/attempts/<hash>.json
```

```
# Steer a worker mid-run (no restart needed)
subagents action:"steer" target:"litmus-worker-arch-1"
  message:"Checkout opt-2's best commit and combine their LR with DEPTH=10."

# Stop everything
subagents action:"kill" target:"all"
```

Or just tell your agent: `"How are my Litmus agents doing?"` / `"Stop all Litmus agents"`.

---

## What Agents Write Overnight

| Path | Written by | Contents |
|---|---|---|
| `shared/attempts/<hash>.json` | Workers | Structured record per experiment — agent, val_bpb, status, title, commit, parent |
| `shared/skills/<name>.md` | Workers + Synthesizer | Validated reusable techniques with YAML frontmatter and evidence commits |
| `shared/notes/discoveries/` | Workers | Per-improvement discovery notes with frontmatter |
| `shared/notes/anomalies/` | Workers + Director | Unexpected result notes |
| `shared/notes/moonshots/` | Leisure + Workers | Speculative hypotheses from overnight thinking |
| `shared/notes/synthesis/` | Synthesizer | Research agenda, combination matrix, exhausted areas |
| `shared/discoveries.md` | Workers | Cross-agent best results (flat, for quick reading) |
| `shared/anomalies.md` | Workers + Director | Unexpected results (flat) |
| `shared/midnight-reflections.md` | Leisure | Nightly reflection narrative |
| `~/.litmus/repo/` (git) | Workers | All experiment commits on per-agent branches |

---

## Research Templates

| Template | Focus |
|---|---|
| `architecture` | Depth, aspect ratio, head dim, WINDOW_PATTERN (SLSL/LSLS/etc) |
| `optimizer` | Per-matrix learning rates, schedule shape, Muon vs AdamW |
| `regularization` | Softcap, gradient clipping, weight decay, residual scaling |
| `general` | Open-ended — combinatorial, tries anything, prefers unexplored combinations |

---

## Requirements

- **OS**: Linux or macOS (Windows not supported)
- **GPU**: NVIDIA with CUDA
- **`uv`**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **`git`**: for experiment version control and worktrees
- **`python3`**: for JSON attempt records and leaderboard scripts

See [INSTALL.md](INSTALL.md) for full details.

---

## License

MIT-0 — do whatever you want with it.
