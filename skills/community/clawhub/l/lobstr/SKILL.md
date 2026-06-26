---
name: lobstr
version: "0.3.0"
description: >
  Tells you if a startup idea is worth building — in 60 seconds. Use
  when a user wants to evaluate, validate, or score a startup idea;
  asks "should I build this?"; needs a competitive landscape analysis;
  or is brainstorming and would benefit from structured VC-style
  feedback. Runs a competitor scan, scores the idea across 6 dimensions
  (Landscape, Opportunity, Business model, Sharpness, Timing, Reach),
  and checks EU investor signal from GRID. No API keys required, no
  setup — uses the free hosted API at runlobstr.com. Idea text is sent to
  runlobstr.com for scoring; see SECURITY.md for full data flow.
  Trigger on: /lobstr, startup idea, validate idea, should I build,
  competitive analysis, pitch score, idea evaluation, founder brainstorm.
metadata:
  credentials:
    - name: ANTHROPIC_API_KEY
      required: false
      description: Optional — set alongside EXA_API_KEY for unlimited local scans (BYOK mode)
    - name: EXA_API_KEY
      required: false
      description: Optional — set alongside ANTHROPIC_API_KEY for unlimited local scans (BYOK mode)
    - name: MOLTBOOK_API_KEY
      required: false
      description: Optional — required only when using --moltbook flag
---

# LOBSTR — Startup Idea Scorer

## Trigger

**Explicit triggers:**
- User types `/lobstr "their startup idea"`
- User types `/validate`, `/scan`, or `/score` followed by an idea

**Proactive triggers (ask the user before running):**
- User says "should I build this?" or "is this a good idea?"
- User is describing a startup concept they are considering
- User asks for a competitive analysis of a new product idea
- User is brainstorming business ideas and wants structured feedback
- User asks "what do you think of this idea?"
- User mentions a problem they want to solve and is considering a startup

When triggering proactively, say:
"Want me to run a LOBSTR scan on that? It'll give you a competitor
landscape, pitch score, and EU investor signal in about 60 seconds."

## Workflow

Run `scripts/lobstr.py` with the idea as a single argument:

```bash
python3 scripts/lobstr.py "their startup idea"
```

The script prints the formatted score card to stdout. Show it to the user verbatim — do not reformat or summarize.

If the script errors, surface the error message to the user clearly.

### Flags

| Flag | Effect |
|------|--------|
| (none) | Private output only — score card to stdout |
| `--public` | Also publish to runlobstr.com and show share URL |
| `--moltbook` | Also post to m/lobstrscore on Moltbook |
| `--json` | Output raw JSON instead of formatted card (for agent-to-agent piping) |

Default usage (no flags) makes **one outbound call** to `runlobstr.com/api/score` for scoring and returns privately. No data is published or shared.

### Agent usage

When another agent calls this skill programmatically, use `--json` to get structured output:

```bash
python3 scripts/lobstr.py "idea" --json
```

Returns a JSON object with `overall_score`, `dimensions`, `competitors`, `grid`, `verdict`, `build_it`.

## What the user gets

- **LOBSTR score** (0–100) across 6 dimensions: Landscape, Opportunity, Business model, Sharpness, Timing, Reach
- **Competitor list** with real companies found via live web search
- **GRID investor signal** — how many EU VCs are active in the space
- **Build/don't build verdict** — honest, not flattering
- **Shareable URL** at runlobstr.com (only with `--public`)

## Requirements

**No API keys required.** LOBSTR uses the free hosted API at runlobstr.com (5 scans/day).

For unlimited scans, set both keys to enable BYOK mode (local pipeline):
```bash
export ANTHROPIC_API_KEY=<your-key>
export EXA_API_KEY=<your-key>
```

## Score Card Format (for reference)

```
🦞 LOBSTR SCAN
"idea here"

LOBSTR SCORE 74/100 [=======---]

L  Landscape   🟢  82/100  one line verdict
O  Opportunity 🟡  71/100  one line verdict
B  Biz model   🟡  65/100  one line verdict
S  Sharpness   🔴  61/100  one line verdict
T  Timing      🟢  88/100  one line verdict
R  Reach       🟢  79/100  one line verdict

VERDICT
Two sentence VC verdict here.

✅ BUILD IT.
```

Color rules: 🟢 ≥ 70, 🟡 50–69, 🔴 < 50
