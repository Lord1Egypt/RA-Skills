---
name: proof-agent
description: Adversarial verification of AI-generated work. Spawns an independent verifier to check for false claims, broken code, and security issues.
---

# Proof Agent

Independent adversarial verification for AI work. The worker and the verifier are always separate agents — self-verification is not verification.

## When to Verify

Verify automatically when:
- Subagent changed **3+ files**
- ANY changed file matches: `*auth*`, `*secret*`, `*permission*`, `Dockerfile`, `*.env*`
- User explicitly asks for verification

Skip verification for:
- Formatting-only changes (whitespace, linting fixes)
- `.gitignore` changes

## How to Verify

1. **Spawn an independent verifier subagent** — the worker CANNOT verify its own work
2. Give the verifier ONLY: the original request, files changed, and approach taken
3. Do NOT share the worker's self-assessment or test results
4. The verifier must run its own commands and provide evidence
5. If no subagent ran (manual changes or user says "verify this"), use `git diff` output as the approach summary

### Verification Prompt

Use this prompt when spawning the verifier subagent:

```
VERIFICATION REQUEST

## Original Request
{what was asked}

## Files Changed
{list of files}

## Approach Taken
{what the worker did — or git diff summary if no subagent ran}

## Your Job

You are an independent verifier. The worker who made these changes CANNOT verify their own work — only you can assign a verdict.

### Review Checklist
1. Correctness: Does the code actually do what was requested?
2. Bugs & Edge Cases: Regressions, unhandled errors, missed cases?
3. Security: Vulnerabilities, exposed secrets, permission issues?
4. Build: Does it build/compile/lint cleanly?
5. Facts: Are any claims, version numbers, or URLs verifiable? Check them.

### Rules
- For EVERY check, include the actual command you ran and its output
- Do NOT take the worker's word for anything
- Do NOT give PASS without running at least 3 verification commands
- You have NO information about the worker's test results — verify independently

## Verdict

Assign EXACTLY ONE verdict as a markdown heading (### PASS, ### FAIL, or ### PARTIAL):

### PASS
All checks passed. Every claim backed by command output.

### FAIL
Issues found. List each as a bullet (- file, line, what's wrong, severity: critical/major/minor).

### PARTIAL
Some passed, some unverifiable. List both with evidence.
```

## Verdicts

- **PASS** — All checks passed with evidence
- **FAIL** — Issues found. Report to user with specifics. Retry up to 3 times if fixable.
- **PARTIAL** — Some checks passed, others couldn't be verified. Report what's unverifiable.

## After Verification

- **PASS**: Report summary to user, proceed
- **FAIL**: Report issues to user. If auto-fixable, spawn worker to fix, then re-verify (max 3 attempts)
- **PARTIAL**: Report to user, let them decide whether to proceed

## Scripts

### `scripts/verify.sh [base-ref]`
Auto-extracts git diff, changed files, commit messages, and sensitive file detection. Outputs a filled verification prompt ready to send to the verifier subagent. Default base: `HEAD~1`.

```bash
bash scripts/verify.sh         # verify last commit
bash scripts/verify.sh main    # verify all changes since main
```

### `scripts/fact-check.sh <file> [file2 ...]`
Extracts and validates factual claims from files:
- URLs → HTTP status check
- npm packages → registry version lookup
- GitHub Actions → tag/SHA existence check

```bash
bash scripts/fact-check.sh src/content/articles/en/my-article.md
bash scripts/fact-check.sh .github/workflows/*.yml
```

Returns exit code 1 if any checks fail.

## Configuration

Projects can customize via `proof-agent.yaml` in the repo root (loaded by `proof_agent/config.py`):

```yaml
thresholds:
  min_files_changed: 3
  always_verify:
    - "**/*auth*"
    - "**/*secret*"
    - "**/*permission*"
    - "**/Dockerfile"
    - "**/*.env*"
  never_verify:
    - "**/.gitignore"

retry:
  max_attempts: 3
  escalate_on_max: true
```

## Key Principle

> The worker and verifier must be separate agents. Self-verification is not verification.
