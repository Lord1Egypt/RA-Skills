---
name: jev-pipeline
description: Use when a codebase has LLM calls that only pick a label, a score, or a yes/no; when deciding whether a task should use Jev / TypeSafe System One instead of a chat model; when drafting or debugging typed Choice/Score/Noul questions; or when calibrating thresholds and escalation bands from logged Jev responses.
---

# Jev pipeline

One workflow for Jev question design: **find → fit → draft → lint → spread → threshold → cascade**. Find decision-shaped LLM calls in a repo, judge whether Jev fits them, draft typed questions from field-tested patterns, lint them, then calibrate on real responses and plan which answers act, pass, or escalate.

## If the CLI is installed

```bash
pip install git+https://github.com/vicfei/jev-pipeline-skill   # stdlib only
python -m jev_pipeline tools-sync   # once: clones the upstream tool repos (MIT, by reference)
```

| Command | Answers | Needs |
|---|---|---|
| `run REPO` | find+fit+draft+lint in one pass | nothing (offline) |
| `find REPO` | which LLM calls output decisions, not text? | nothing |
| `fit` | go / go-with-guards / no-go per candidate | editable `*.answers.json` |
| `draft` | first question template per candidate | nothing |
| `lint` | does the draft break known rules? | nothing |
| `spread RESPONSES.jsonl` | does the question discriminate or is it constant? | logged responses |
| `threshold SCORES.jsonl` | where does the bar go, fitted on hard cases? | labeled scores |
| `cascade SCORES.jsonl` | act / pass / escalate plan | scores |

State and reports land in `--out` (default `./jev-pipeline-out/`). No step calls an API.

## If it is not installed — the rules that matter

**Fit (should this be Jev at all?):** output is a decision from a closed set (≤255 options, 2–10 levels, or yes/no) → maybe. Plain code/regex could decide it exactly → no. The decision needs math, counting, or date comparison → no (compute in code, judge the meaning). Input is text and fits ~32k tokens → yes. High volume and latency-sensitive → Jev's territory.

**Drafting:** atomic judgments only — one narrow question each, many per request, evaluated independently. Choice always carries an escape option (`other` / `review`). Score criteria are a strictly ordered rubric. Noul states one checkable proposition. Variable content goes in `state`; question text stays byte-stable because thresholds depend on it.

**The ten ways questions go wrong:** (1) asking Jev to compute; (2) Choice without an escape; (3) Score with an unordered rubric; (4) reading Noul 0.5 as "medium" — it means *can't tell*; (5) one global threshold everywhere; (6) trusting `jev-latest` when thresholds matter — pin `jev-1.13.0`, log the returned version; (7) ignoring probabilities when the top two are 0.45/0.42; (8) questions owning side effects; (9) using Jev as authorization; (10) open-ended "Choice" with unbounded options.

**Cascade policy:** two bands, not three verdicts. Act on the top band, pass the bottom, and treat the middle — and any low-confidence top — as an explicit escalation branch to a System Two model or a human. Never average uncertainty into a decision.

## Sources and attribution

Patterns condensed from [awesome-jev-prompts](https://github.com/vicfei/awesome-jev-prompts) (CC0). Steps call upstream tools by reference, never copied: [abhisheksharma001/jev-skill](https://github.com/abhisheksharma001/jev-skill) (find, fit) and [VBS2004/jev-questions-skill](https://github.com/VBS2004/jev-questions-skill) (lint, spread, threshold, coverage) — see the repo's ATTRIBUTION.md. Independent community project, not affiliated with TypeSafe AI.
