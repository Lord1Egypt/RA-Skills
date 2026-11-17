# Validate fixes with AutoFix & experiments (step 6)

> **Availability:** AutoFix is rolling out. If `POST /v1/autofix/*` routes return 404 on
> the org, the feature isn't enabled yet — skip to `apply-fixes.md` and label fixes as
> "diagnosed, not backtested". Do not fake validation.

AutoFix takes a NovaPilot report and **backtests** candidate fixes: it replays the failing
calls under each candidate prompt on the customer's own model, re-scores both legs with
the same eval scorers, evolves candidates, and validates champions on a held-out split
with statistical gates (bootstrap CI + A/A noise floor). The output is fixes with
evidence, not suggestions.

## Run AutoFix from a report

```
POST /v1/autofix/run
{ "preset": "balanced",            // quick | balanced | thorough | deep
  "datasetSlug": "<slug>", "sourceReportId": "<novapilot reportId>" }
→ poll the run's status via the runs LIST (summaries), until terminal (deep runs on
  large fleets can take hours — prefer quick/balanced interactively; schedule deep runs)
```

**The completed run's state/quality report is hundreds of KB to MB — never fetch it
inline.** Stream it to disk
(`python scripts/fetch_to_file.py "/v1/autofix/runs/<id>" --out /tmp/autofix.json`) and
read selectively: `summary` → `recommendations[]` → per-rec `diff`/evidence on demand
(see `context-safety.md`).

In the quality report, `recommendations[]` carry `diff` objects —

```json
"diff": { "kind": "search-replace" | "append-rule",
          "search": "<verbatim substring or null>", "replace": "<new text>",
          "rule": "<narrative rule>",
          "basePrompt": "<prompt as measured>", "fixedPrompt": "<prompt after fix>" }
```

plus per-fix validation labels (validated win / directional / regression) and
`experiments[]` (everything tried, with per-scorer before→after deltas).

## Author your own experiments (test a specific hypothesis)

Experiments are drafts until a human approves — authoring is free, running costs credits.

```
POST /v1/autofix/runs/:runId/experiments
{ "experiments": [
    { "id": "exp_1", "type": "prompt.searchReplace",
      "label": "Force KB lookup before answering",
      "agentName": "<agent>",                       // multi-agent fleets
      "affectedScorers": ["faithfulness"],
      "edit": { "search": "<verbatim substring of the live system prompt>",
                "replace": "<replacement text>" } },
    { "id": "exp_2", "type": "prompt.append",
      "label": "Mandatory closing phrase",
      "replace": "<rule text appended to the prompt>",
      "affectedScorers": ["instruction_adherence"] } ] }
```

Rules:
- `search` must be copied **character-for-character** from the current prompt (get it from
  the NovaPilot report's `currentPrompt`); a non-matching search no-ops.
- The user must approve drafts before they run (the API enforces this) — present the
  drafts, get approval, then trigger. **Poll status on the runs LIST (summaries), never
  the by-id run endpoint** (it inlines the full state).
- Once terminal, read experiment results from the state file you already downloaded
  (`fetch_to_file.py` as above) — per experiment: `outcome`, `objectiveGain`,
  `validatedWin`, per-scorer deltas, regressions, held-out N. Report them honestly,
  including losses.

## Compare & verify (closing the loop)

- `GET /v1/autofix/runs/:runId/compare` — health delta vs the baseline run (did things
  actually improve run-over-run).
- After a fix ships to production (step 7), the verify endpoint re-scores fresh post-apply
  traffic against the run's pre-fix health — this is the ground-truth check that the fix
  worked in the real world, not just in backtest.

## Which fixes to carry into step 7

Only: (a) validated wins, (b) directional improvements the user explicitly accepts, and
(c) NovaPilot recommendations the user accepts un-backtested (label them as such in the PR).
Never carry a fix the backtest flagged as a regression.
