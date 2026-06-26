```skill
---
name: know-your-ai
description: AI security testing & evaluation CLI. Run red-team evaluations, check vulnerabilities, and review results for your AI products.
homepage: https://knowyourai.hydrox.ai
requires:
  bins:
    - node
  env:
    - KNOW_YOUR_AI_DSN
primaryEnv: KNOW_YOUR_AI_DSN
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["node"],"env":["KNOW_YOUR_AI_DSN"]},"primaryEnv":"KNOW_YOUR_AI_DSN"}}
---

# Know Your AI

AI security testing and evaluation CLI by [HydroxAI](https://hydrox.ai). Run red-team evaluations, detect jailbreak vulnerabilities, and review security scores for your AI products — all from the command line.

## Check setup

```bash
node {baseDir}/scripts/doctor.mjs
```

Validates your DSN configuration and tests API connectivity. Requires `KNOW_YOUR_AI_DSN` environment variable.

## Show linked product & connection

```bash
node {baseDir}/scripts/target.mjs
```

## List evaluations and datasets

```bash
node {baseDir}/scripts/list.mjs
```

## Run an evaluation

```bash
node {baseDir}/scripts/evaluate.mjs <evaluation-id>
node {baseDir}/scripts/evaluate.mjs <evaluation-id> --max-prompts 5
node {baseDir}/scripts/evaluate.mjs <evaluation-id> --timeout 300
```

Triggers an evaluation run and streams real-time progress. Returns scores, pass/fail counts, and the run ID.

### Options

- `--max-prompts <n>`: Maximum prompts per dataset (default: 3)
- `--timeout <seconds>`: Maximum wait time in seconds (default: 600)
- `--debug`: Enable debug logging

## View run history

```bash
node {baseDir}/scripts/history.mjs
node {baseDir}/scripts/history.mjs --all
```

- `--all` / `-a`: Show all runs (default: last 10)

## View results of a specific run

```bash
node {baseDir}/scripts/result.mjs <run-id>
```

## Describe an evaluation

```bash
node {baseDir}/scripts/describe.mjs <evaluation-id>
```

Shows detailed evaluation configuration: judge model, threshold, linked datasets, and prompt counts.

## Notes

- Requires `node` (>=18) runtime
- Requires `KNOW_YOUR_AI_DSN` environment variable from the Know Your AI dashboard (Settings → API Keys)
- DSN format: `https://kya_xxx:da2-xxx@host/product_id`
- Short alias `kya` is also available if installed globally via npm
- Use `doctor` first to verify connectivity before running evaluations
- Review detailed results in the Know Your AI dashboard after runs complete
```
