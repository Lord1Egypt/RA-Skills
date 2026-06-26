---
name: openclaw-scheduler-token-auditor
description: Audit OpenClaw scheduler token usage for cron jobs, scheduled tasks, and heartbeat sessions. Use when the user wants to know which scheduled job is expensive, which cron is burning the most tokens, whether a cron or heartbeat run exceeds a token threshold or budget, why scheduler token usage is high, or to investigate unexpected token burn. Trigger explicitly on slash-style phrases like "/token_auditor" and "/schedule_auditor". Also match requests such as "audit scheduler tokens", "which cron uses the most tokens", "check whether this scheduled task exceeds 50000 tokens", "audit heartbeat token usage", "find expensive scheduled tasks", "查哪个 cron 最烧 token", or "检查这个定时任务有没有超 token".
---

# OpenClaw Scheduler Token Auditor

Audit scheduler token usage conservatively. Separate what is **measured**, what is only **bounded**, and what remains **unknown**.

## What this skill is for

Use this skill to answer questions like:

- Which cron job is burning the most tokens?
- Did this scheduled task exceed 50000 tokens per run?
- Is heartbeat usage actually expensive, or does it only look scary?
- Why did scheduler token usage spike?
- Audit all scheduled tasks against a custom threshold such as 80000 or 120000 tokens.

## How users typically trigger it

This skill should trigger for requests such as:

- `/token_auditor`
- `/schedule_auditor`
- `Audit scheduler token usage`
- `Find expensive cron jobs`
- `Check whether this cron exceeds 50000 tokens`
- `Investigate unexpected token burn in scheduled tasks`
- `Audit heartbeat token usage`
- `Which scheduled runs are the costly ones?`

If the user gives no threshold, use **50000 tokens per run**.

## Core rule set

1. **For cron runs, only `usage.total_tokens` is authoritative.**
   Do not replace it with hand-summed `input + output` values.
2. **Session status, session lists, and transcripts are supporting evidence.**
   Use them to explain a result, not to manufacture one.
3. **Missing usage means unknown.**
   If a run lacks `usage.total_tokens`, do not call it cheap or safe.
4. **Heartbeat analysis is usually bounded, not exact.**
   Without explicit usage fields, you may rule out obviously huge per-run usage, but you may not claim an exact token count.
5. **State the threshold explicitly.**
   Default to 50000 unless the user specifies another threshold.
6. **Do not invent commands or undocumented fields.**
   Prefer first-class OpenClaw tools.

## Evidence classes

Use exactly one label per audited target:

- **Exact** — authoritative token count exists, usually from `usage.total_tokens`
- **Bounded** — no exact count, but current evidence safely rules out obvious extreme usage
- **Inconclusive** — required evidence is missing, so no safe token claim can be made

## Audit workflow

### 1) Classify the target

Separate the audit by evidence type:

- **Cron jobs**
- **Heartbeat sessions**

Do not blur them into one vague conclusion.

### 2) Audit cron jobs

Preferred path:

- `cron(action="list")`
- `cron(action="runs", jobId=..., limit=...)`

Procedure:

1. Identify the relevant cron job or jobs.
2. Fetch recent run records.
3. Read `usage.total_tokens` from each run.
4. Compare each exact count to the active threshold.
5. Only after that, inspect session metadata or transcripts to explain *why* a verified expensive run happened.

CLI fallback only if needed:

```bash
openclaw cron list
openclaw cron runs --id <jobId> --limit 50
```

Interpretation:

- Has `usage.total_tokens` -> **Exact**
- Missing `usage.total_tokens` -> **Inconclusive**
- Never substitute transcript size or `input + output`

### 3) Explain expensive cron runs

Once a run is already verified as expensive, look for causes such as:

- oversized prompts or task scope
- repeated large file reads, web fetches, or tool outputs
- session reuse that drags in extra context
- retries, loops, or obvious workflow mistakes

These are explanations for an exact finding, not substitutes for exact usage.

### 4) Audit heartbeat sessions

Treat heartbeat as **bounded-risk analysis** unless explicit usage data exists.

Useful checks:

- `sessions_list` to find heartbeat sessions
- `session_status` to inspect context accumulation
- `sessions_history` to inspect recent transcript size, repetition, and tool fan-out

A **Bounded** conclusion is reasonable when the observed pattern shows:

- little or no context accumulation
- short repetitive turns
- small reads and short outputs
- no evidence of large injected context or wide fan-out

Without explicit usage, phrase conclusions like:

- `No evidence of 50000+-per-run behavior`
- `Observed structure appears lightweight`
- `Exact per-run tokens are unavailable`

## Decision rules

### Cron with `usage.total_tokens`

Allowed:

- exact per-run token counts
- threshold pass/fail verdicts
- comparisons across runs
- trend summaries grounded in run records

Not allowed:

- replacing the total with hand-summed fields
- estimating totals from transcript size

### Cron without `usage.total_tokens`

Allowed:

- `Inconclusive`
- structural observations that help future debugging

Not allowed:

- claiming the run is cheap, safe, or below threshold
- assigning a token number from side evidence

### Heartbeat without explicit usage

Allowed:

- bounded statements such as `current evidence rules out obvious 80000+-per-run behavior`
- structural explanations for that bounded conclusion

Not allowed:

- exact per-run token counts
- exact cumulative totals inferred from transcripts alone

## Output pattern

Always state the threshold used.

Examples:

- `Threshold used: 50000 tokens per run`
- `Threshold used: 80000 tokens per run`

For each target, report:

- target name
- target type: `cron` or `heartbeat`
- evidence class: `Exact`, `Bounded`, or `Inconclusive`
- token finding
- threshold verdict: pass, fail, or unknown
- concise cause analysis when evidence supports it

Example phrasings:

- **Exact** — `Nightly report cron — Exact — 158784 tokens on the latest run — exceeds 50000.`
- **Bounded** — `Main heartbeat — Bounded — observed structure rules out obvious 80000+-per-run behavior, but exact per-run tokens are unavailable.`
- **Inconclusive** — `Daily digest cron — Inconclusive — run record lacks usage.total_tokens, so the threshold result is unknown.`

## Failure modes to avoid

1. **Hand-sum trap** — `input + output` may disagree with `usage.total_tokens`
2. **Missing-data optimism** — missing usage is not low usage
3. **Transcript-as-meter trap** — transcript size is not a billing source
4. **Heartbeat overclaim** — lightweight structure supports bounded conclusions, not exact counts
5. **Mixed-evidence blur** — do not merge Exact cron findings and Bounded heartbeat findings into one vague claim
6. **Invented-command trap** — if CLI syntax is uncertain, check docs or `openclaw help` first
7. **Threshold drift** — always say whether the threshold was default or user-specified

## Minimal examples

### Exact cron result

A run record contains `usage.total_tokens: 158784`, and the user gave no threshold.

Correct conclusion:

- threshold used: `50000`
- evidence class: `Exact`
- verdict: `exceeds 50000`

### Custom threshold

A run record contains `usage.total_tokens: 47617`, and the user asks for `80000`.

Correct conclusion:

- threshold used: `80000`
- evidence class: `Exact`
- verdict: `does not exceed 80000`

### Misleading hand-sum

A run shows `input_tokens: 49680` and `output_tokens: 9612`, while the authoritative record says `usage.total_tokens: 47617`.

Correct conclusion:

- use `47617`
- do **not** report `59292`

### Bounded heartbeat result

A heartbeat session shows near-zero context accumulation and a repeating pattern of small checklist reads plus short acknowledgements.

Correct conclusion:

- evidence class: `Bounded`
- `no evidence of <threshold>+-per-run behavior`
- `exact per-run tokens unavailable`

### Missing usage

A cron run exists but the record has no `usage.total_tokens`.

Correct conclusion:

- evidence class: `Inconclusive`
- verdict: `unknown`
- next step: investigate provider support, run logging, or other authoritative records
