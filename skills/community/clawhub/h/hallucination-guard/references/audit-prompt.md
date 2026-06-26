# Cross-Model Audit Prompt

## Spawn Template

```
sessions_spawn:
  task: (see below)
  mode: "run"
  model: "gemini"  # cheapest model that can verify
  label: "audit_{topic}_{date}"
```

### Task Prompt — File/Artifact Verification

```
You are an independent auditor. Your job is to verify claims against physical evidence.

CLAIMS TO VERIFY:
{list_of_claims}

INSTRUCTIONS:
1. For each claim, use the `read` or `exec` tool to check the physical artifact
2. Do NOT trust the claims — verify independently
3. Report format:

CLAIM: {claim text}
EVIDENCE: {what you found}
VERDICT: CONFIRMED / CONTRADICTED / UNVERIFIABLE
DETAILS: {specifics}

If any claim is CONTRADICTED, flag it prominently at the top of your response.
```

### Task Prompt — Data Report Verification

```
You are an independent data auditor.

SOURCE FILE: {path_to_csv_or_data}
CLAIMS TO VERIFY:
- Total records: {claimed_count}
- Key metric: {claimed_value}
- Summary: {claimed_conclusion}

INSTRUCTIONS:
1. Read the source file with `read` tool
2. Count records yourself: `exec wc -l {path}`
3. Calculate the metric yourself from raw data
4. Compare your results to the claims

Report each claim as CONFIRMED or CONTRADICTED with your own calculated values.
```

### Task Prompt — Git Verification

```
You are verifying git claims.

CLAIMS:
- Committed to branch: {branch}
- Commit message: {message}
- Files changed: {files}

INSTRUCTIONS:
1. Run: git log --oneline -5
2. Run: git diff HEAD~1 --name-only
3. Run: git show HEAD --stat
4. Compare actual git state to claims.

Report: CONFIRMED or CONTRADICTED for each claim.
```

## Model Selection Guide

| Verification Type | Recommended Model | Why |
|-------------------|-------------------|-----|
| File exists, content check | flash/gemini | Simple tool calls |
| Numeric calculation audit | gemini/sonnet | Needs arithmetic |
| Logic/architecture review | sonnet/opus | Needs reasoning |
| Code correctness | sonnet | Needs code understanding |

**Default to the cheapest model.** Upgrade only when the verification requires reasoning, not just tool use.

## Cost Estimation

- Flash audit: ~$0.001 per verification (1-3 tool calls)
- Gemini audit: ~$0.005 per verification
- Sonnet audit: ~$0.05 per verification
- Opus audit: ~$0.50 per verification (use sparingly)

Typical workflow: 1 flash audit per task = negligible cost increase.
