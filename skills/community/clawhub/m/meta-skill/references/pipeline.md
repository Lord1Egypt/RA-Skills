# Meta‑Skill — Trajectory Compiler

## Purpose
Compile a concrete execution trace into a parameterized OpenClaw Skill via a full 4‑stage pipeline:
1) Trace interception → 2) DAG abstraction → 3) Schema + code synthesis → 4) Registration & hot reload.

---

## Stage 1 — Trace Interception (implemented)
Two ways to generate **real** traces:

### A) From JSONL tool-call events
**Script:** `scripts/trace-interceptor.js`

**Input:** JSONL events from your tool middleware/logging
```bash
node scripts/trace-interceptor.js --in /path/to/events.jsonl --out /tmp/trace.json --name my-skill
```

### B) From OpenClaw session transcripts (REAL)
**Script:** `scripts/trace-from-session.js`

This reads OpenClaw’s session JSONL and extracts actual tool calls + tool results.

**Latest session:**
```bash
node scripts/trace-from-session.js --latest --out /tmp/trace.json --name my-skill
```

**Specific session file:**
```bash
node scripts/trace-from-session.js --session /path/to/session.jsonl --out /tmp/trace.json
```

**Time window:**
```bash
node scripts/trace-from-session.js --latest --since "2026-03-12T00:00:00Z" --until "2026-03-12T02:00:00Z" --out /tmp/trace.json
```

---

## Stage 2 — DAG Construction & Abstraction (implemented)
**Script:** `scripts/trajectory-compiler.js`

- Builds DAG from `__ref__` and template references.
- Lifts variable inputs into schema parameters.
- Enforces no hard‑coded dependency values.

---

## Stage 3 — Schema + Code Synthesis (implemented)
**Outputs:**
- `references/schema.json`
- `references/plan.json`
- `references/run-flow.md` (human-readable run flow)
- `scripts/run.js`

Run script includes error handling, missing dependency checks, and optional retry hooks.

---

## Stage 4 — Registration & Hot Reload (implemented)
**Compiler output:** writes into OpenClaw skills directory
- Default: `~/.openclaw/workspace/skills/<skill-name>`
- Override: `--out /path/to/skills`

You may need to refresh Skills or restart Gateway to load.

---

## Full Pipeline Usage
```bash
# 1) Intercept trace (real session)
node scripts/trace-from-session.js --latest --out /tmp/trace.json --name my-skill

# 2) Compile into skill
node scripts/trajectory-compiler.js --trace /tmp/trace.json --out ~/.openclaw/workspace/skills
```
