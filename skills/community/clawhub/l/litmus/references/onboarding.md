# Litmus Onboarding

Run this when the user asks to set up Litmus for the first time — or when they say something like
"install Litmus", "set up Litmus on this machine", or "get autoresearch running".

---

## Step 1 — System check

Run these silently before talking to the user.

**GPU:**
```bash
nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader 2>/dev/null
```

**Dependencies:**
```bash
uv --version 2>/dev/null && echo "uv ok" || echo "uv missing"
git --version 2>/dev/null && echo "git ok" || echo "git missing"
claude --version 2>/dev/null && echo "claude ok" || echo "claude missing"
```

**Interpret GPU output:**
| VRAM / count | Suggested agents |
|---|---|
| No GPU / command not found | Block — tell user Litmus requires an NVIDIA GPU |
| 1 GPU < 8 GB | 1 agent (warn: slow) |
| 1 GPU 8–16 GB | 1–2 agents |
| 1 GPU 16–24 GB | 2–3 agents |
| 1 GPU > 24 GB, or 2 GPUs | 3–4 agents |
| 3+ GPUs | 1 agent per GPU |

If `uv` is missing: block — tell the user to install it first:
`curl -LsSf https://astral.sh/uv/install.sh | sh`

Note whether `claude` CLI is available — it affects the runtime recommendation below.

---

## Step 2 — Config conversation

Present all defaults in a single message so the user can say "looks good, start" without answering
anything. Only go deeper if they want to change something.

Template for the opening message:

---

> Here's what I'd configure for your machine. Say **"go"** to use all defaults, or tell me what
> to change.
>
> **Your system:** [GPU name] ([VRAM]) × [count] — [N] agents recommended
>
> **Schedule** *(all times local — tell me your timezone first)*
> ```
> 03:00  Leisure      workers enter creative mode (papers, moonshots, gap analysis)
> 04:00  Synthesizer  distills overnight notes into the skills library
> 06:00  Dawn         workers wake, pick up experiment queue
> 08:00  Digest       morning research narrative delivered to you
> Every 2h  Director  steers workers, triggers pivots on stagnation
> Every 30m Watchdog  liveness + escape mode if no progress
> ```
> These are the defaults — you can shift any of them. Common adjustments:
> - Short nights (e.g. wake at 05:00): leisure 01:00 → synth 02:00 → dawn 03:00 → digest 06:00
> - Want more thinking time: extend leisure window (e.g. 02:00–07:00, synth at 04:00)
> - Want frequent steering: director every 1h instead of 2h
>
> **Agents & compute**
> - Number of agents: **[GPU-based recommendation]**
> - Experiment time budget: **5 min** per run — quick check at 90s cuts dead ends early
> - Runtime: **native subagents** (OpenClaw sessions_spawn) ← recommended
>   *(Claude Code sessions also available — [available/not found on this machine])*
>
> **Research focus**
> - Templates: **[recommended based on agent count]**
>   *(architecture · optimizer · regularization · general — mix as needed)*
> - Custom research goal: *none* — agents explore freely
> - Areas to skip: *none*
>
> **Leisure intensity**
> - arxiv searches per night: **3**, up to **5 papers** each
> - Moonshot hypotheses generated: **5**
> - Contradiction analysis: **on**
>
> **Notifications**
> - New global best: **on** (immediate ping)
> - Agent crash: **on**
> - Stagnation alerts: **off**
>
> **ClawRxiv** *(optional — agents publish research papers here)*
> - Status: **disabled** — enable if you want agents to auto-publish discoveries
> - Publishes on: new global best (always), leisure analysis (optional)
> - Requires a free ClawRxiv API key — I can register one for you during setup
>
> What's your timezone, and anything you'd like to change?

---

### Config questions — go deeper only if the user asks

#### Timing

The six scheduled events form a chain. Explain this chain if the user wants to shift times:

```
[research]──────────────────────[Leisure]──[Synth]──[Dawn]──────[Digest]
              Director every Nh  03:00      04:00    06:00        08:00
```

Rules:
- **Leisure start** can be anything — pick when the GPU would otherwise sit idle
- **Synthesizer** must be ≥ 30 min after leisure start (workers need time to write notes first)
- **Dawn** must be ≥ 30 min after synthesizer (workers need the skills library ready before resuming)
- **Digest** can be any time after dawn — earlier means a shorter overnight window
- **Director** covers the research window (dawn → leisure start); interval of 1h = more responsive, 4h = less overhead
- **Watchdog** is independent — 15 min catches problems faster, 60 min is quieter

| Setting | Default | Fast/intensive | Night-shift | Notes |
|---|---|---|---|---|
| Leisure start | 03:00 | 01:00 | 22:00 | When experiments stop, thinking begins |
| Synthesizer | 04:00 | 02:00 | 23:30 | Must be inside leisure window |
| Dawn | 06:00 | 03:30 | 01:00 | Ends leisure window |
| Digest | 08:00 | 06:00 | 07:00 | When you want the report |
| Director interval | 2h | 1h | 3h | Shorter = more steering overhead |
| Watchdog interval | 30 min | 15 min | 60 min | Shorter = faster crash detection |

If the user is non-technical, offer three preset schedules instead of individual settings:

| Preset | Leisure | Synth | Dawn | Digest | Director |
|---|---|---|---|---|---|
| **Standard** (default) | 03:00 | 04:00 | 06:00 | 08:00 | 2h |
| **Night owl** (stays up late) | 01:00 | 02:00 | 04:00 | 07:00 | 2h |
| **Early bird** (wakes at 5am) | 23:00 | 00:30 | 02:00 | 05:30 | 2h |
| **Intensive** (max steering) | 03:00 | 04:00 | 06:00 | 08:00 | 1h |
| **Light** (minimal overhead) | 03:00 | 04:30 | 06:00 | 08:00 | 4h |

#### Agents & compute

| Setting | Default | Notes |
|---|---|---|
| Agent count | GPU-based | Each agent needs ~4 GB VRAM for small LM training |
| Time budget | 300s (5 min) | 180s = fast iteration; 600s = more signal per run |
| GPU assignment | auto | Or explicit: "agent 1 on GPU 0, agent 2 on GPU 1" |

**Runtime mode:**
- `subagents` (default, recommended) — native OpenClaw `sessions_spawn`. Lifecycle managed by
  `subagents` tool. Steer, list, kill work out of the box. No extra setup.
- `claude-code` — spawns persistent Claude Code sessions. Better if the user wants isolated
  terminal-level control or is running Litmus outside of an OpenClaw session. Requires `claude`
  CLI installed. If not found on this machine, don't offer it.

#### Research focus

**Templates** — pick one per agent, or let the user describe their goal in plain language and
map it yourself:
- `architecture` — depth, aspect ratio, head dim, attention window patterns (SLSL/LSLS/etc)
- `optimizer` — per-matrix learning rates, schedule shape, Muon vs AdamW, optimizer internals
- `regularization` — softcap, gradient clipping, weight decay, residual scaling, norm structure
- `general` — open-ended; tries anything; good for combinatorial experiments

Recommended mixes:
- 1 agent: `general`
- 2 agents: `architecture, general`
- 3 agents: `architecture, optimizer, general`
- 4 agents: `architecture, optimizer, regularization, general`

**Custom goal** (optional) — user can say something like:
> "I want to focus on attention mechanisms and anything related to small model efficiency"

Write this verbatim into the agent's `program.md` as a top-level goal. It doesn't replace the
template; it supplements it.

**Areas to avoid** (optional) — user can say:
> "Don't touch tokenization, don't experiment with vocab size"

Write these as explicit constraints in each agent's `program.md`.

#### Leisure intensity

| Level | arxiv searches | Papers per search | Moonshots | Use when |
|---|---|---|---|---|
| light | 2 | 3 | 3 | Short leisure window (< 2h) or limited tokens |
| standard | 3 | 5 | 5 | Default — good balance |
| deep | 5 | 8 | 10 | Long leisure window, want thorough nightly review |

The user can also just say "light", "standard", or "deep" — map it to the numbers above.

#### Notifications

- `onNewGlobalBest` (default: on) — immediate ping any time an agent sets a new all-time best
- `onCrash` (default: on) — ping if a worker session dies unexpectedly
- `onStagnation` (default: off) — ping when all agents plateau for > 3 hours
- `onLeisureComplete` (default: off) — brief ping at 06:00 summarising overnight ideas

---

## Step 3 — Write config

Once you have the user's answers, write `~/.litmus/config.json`. Start from the defaults in
`{baseDir}/configs/default.json` and overwrite with the user's choices.

Example:
```json
{
  "schedule": {
    "timezone": "Europe/London",
    "leisureStart": "03:00",
    "synthesizerTime": "04:00",
    "dawnTime": "06:00",
    "digestTime": "08:00",
    "directorIntervalHours": 2,
    "watchdogIntervalMinutes": 30
  },
  "compute": {
    "agents": 3,
    "timeBudgetSeconds": 300,
    "quickCheckSeconds": 90,
    "gpuAssignment": "auto"
  },
  "research": {
    "templates": ["architecture", "optimizer", "general"],
    "focusAreas": ["attention mechanisms", "small model efficiency"],
    "avoidAreas": [],
    "customGoal": "Focus on attention mechanisms and small model efficiency."
  },
  "leisure": {
    "intensity": "standard",
    "arxivSearchesPerSession": 3,
    "papersPerSearch": 5,
    "moonshotHypotheses": 5,
    "contradictionAnalysis": true
  },
  "notifications": {
    "onNewGlobalBest": true,
    "onStagnation": false,
    "onCrash": true,
    "onLeisureComplete": false
  },
  "runtime": {
    "mode": "subagents",
    "claudeCodePath": "claude"
  },
  "clawrxiv": {
    "enabled": false,
    "agentName": "",
    "apiKey": "",
    "publishOnGlobalBest": true,
    "publishLeisurePapers": false,
    "tags": ["litmus", "autonomous-research", "language-models"]
  }
}
```

**If the user enabled ClawRxiv**: register an agent identity and write the key into config.

Ask for a name to use on ClawRxiv (suggest `litmus-<their username>`), then:
```bash
curl -s -X POST https://clawrxiv.io/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"claw_name\": \"<chosen-name>\"}" | jq .
```

Copy the returned `api_key` into `clawrxiv.apiKey` and set `enabled: true`. Warn: the key is
shown only once. If they already have a key, skip registration and write it directly.

If ClawRxiv is disabled, leave the block with defaults (`enabled: false`).

---

## Step 4 — Run setup

```bash
bash {baseDir}/scripts/setup.sh
```

This clones the training harness to `~/.litmus/harness/`, runs `uv sync`, and downloads ~1 GB of
training data. Tell the user this takes ~5 minutes.

Skip if `~/.litmus/harness/.git` already exists — say so and continue.

---

## Step 5 — Prepare agent workspaces

Read agent count, templates, and time budget from the config you wrote. Pass them to the script:

```bash
bash {baseDir}/scripts/prepare-agents.sh \
  --agents 3 \
  --templates architecture,optimizer,general \
  --time-budget 300
```

The script will print the exact `sessions_spawn` (or `claude` CLI) commands for each agent.
If `customGoal` or `avoidAreas` are set, append them as text to each agent's `program.md` after
the script runs:

```bash
echo "\n## Research Goal\n$CUSTOM_GOAL" >> ~/.litmus/agents/<id>/program.md
echo "\n## Do Not Explore\n$AVOID_AREAS" >> ~/.litmus/agents/<id>/program.md
```

---

## Step 6 — Spawn research agents

**Subagents mode** (default):

```
sessions_spawn
  task: "You are autonomous ML research agent 1 of 3. Read program.md in your working directory
         and begin the research loop immediately. Loop forever."
  runtime: "subagent"
  mode: "session"
  agentId: "litmus-worker-arch-1"
  cwd: "~/.litmus/agents/arch-1"
```

Repeat for each agent.

**Claude Code mode** (if runtime.mode == "claude-code"):

```bash
claude --session-id "litmus-worker-arch-1" \
       --cwd ~/.litmus/agents/arch-1 \
       --print "Read program.md and run the research loop forever." &
```

Repeat for each agent. Note PIDs for manual management (`subagents` tool won't manage these).

After spawning all agents:
```
sessions_yield message: "Research agents are running. I'll send you a digest at 08:00."
```

---

## Step 7 — Register cron jobs

Read all timing values from the config you wrote. Pass them as flags — the script computes
the cron expressions correctly for any combination of times:

```bash
bash {baseDir}/scripts/setup-cron.sh \
  --timezone       "Europe/London" \
  --leisure-start  "03:00" \
  --synthesizer-time "04:00" \
  --dawn-time      "06:00" \
  --digest-time    "08:00" \
  --director-hours 2 \
  --watchdog-minutes 30
```

The script prints 6 cron job definitions. Run each `cron action:"add"` call.
Only pass the flags that differ from defaults — omitted flags use the script's built-in defaults.

---

## Step 8 — Confirm and yield

```
✅ Litmus is running.

3 agents: litmus-worker-arch-1 (architecture), litmus-worker-opt-2 (optimizer), litmus-worker-gen-3 (general)
03:00 Leisure → 04:00 Synthesizer → 06:00 Dawn → 08:00 Digest (Europe/London)
Director every 2h · Watchdog every 30min

Config saved at ~/.litmus/config.json — edit any time and restart to apply changes.

"How are the agents doing?" → status
"Show me results" → leaderboard
"Stop everything" → kills all agents and disables cron
```

---

## Tone guidelines

- Present all defaults upfront — let "go" be a valid answer.
- Be specific on GPU assessment. "Your 4090 can comfortably run 3 agents" not "it depends."
- For the runtime choice, recommend subagents clearly. Only mention claude-code if `claude` is installed.
- Don't explain the research loop — that's in SKILL.md. Onboarding is about config.
- If setup was run before, say so and skip the download step.
