---
name: openmath-open-theorem
description: Queries open formal verification theorems from the OpenMath platform. Use when the user asks for a list of open theorems, wants Lean or Rocq-specific theorems, needs full detail for a theorem ID, or wants to download a theorem and scaffold a local proof workspace.
version: v1.0.0
---

# OpenMath Open Theorem

## Instructions

Query the OpenMath library to discover and scaffold open theorems. The discovery scripts use `OPENMATH_SITE_URL` and `OPENMATH_API_HOST` when set, and otherwise fall back to the default production endpoints.

### First-run gate

Before discovery on a new machine or workspace, check the shared `openmath-env.json`. Auto-discovery only checks `./.openmath-skills/openmath-env.json` and `~/.openmath-skills/openmath-env.json`.

This gate is mandatory. If `openmath-env.json` is missing, or if it exists but `preferred_language` is missing, stop. Do not query the OpenMath theorem list, theorem detail, or download APIs until setup is complete.

If no config exists, stop and ask the user where to create it, then collect at least:

- `preferred_language`: `lean` or `rocq`
- config visibility / save scope: `./.openmath-skills` or `~/.openmath-skills`
- the submit/authz fields only if the user wants end-to-end submission later

Command:

```bash
python3 scripts/check_openmath_env.py
```

### Workflow checklist

- [ ] **Env**: Run `check_openmath_env.py`. If `openmath-env.json` is missing from `./.openmath-skills` and `~/.openmath-skills`, or `preferred_language` is missing, ask the user to finish setup before continuing.
- [ ] **Explore**: Run `fetch_theorems.py [language]` only after the first-run gate passes. If no language is passed, it uses `preferred_language` from `openmath-env.json` and must not fan out to other languages automatically.
- [ ] **Detail**: Run `fetch_theorem_detail.py <id>` only after the first-run gate passes.
- [ ] **Download**: Run `download_theorem.py <id>` only after the first-run gate passes.
- [ ] **Prove**: Use the `openmath-lean-theorem` skill for environment setup, preflight checks, and proving.
- [ ] **Submit**: Use the `openmath-submit-theorem` skill to hash and submit the proof.
- [ ] **Verify**: Run `fetch_theorem_detail.py <id>` and confirm your address is the prover and status is verified.
- [ ] **Claim**: Use the `openmath-claim-reward` skill to generate the withdrawal command.

### Scripts

| Script | Command | Use when |
|--------|---------|----------|
| Shared env check | `python3 scripts/check_openmath_env.py [--config <path>]` | Mandatory first-run gate; validates shared config, preferred language, and the resolved OpenMath website/API endpoints. |
| List open theorems | `python3 scripts/fetch_theorems.py [--config <path>] [language]` | Listing or filtering open theorems after the first-run gate passes. `language`: optional `lean` or `rocq`. Without an explicit CLI language, query only the configured `preferred_language`. |
| Theorem detail | `python3 scripts/fetch_theorem_detail.py [--config <path>] <id>` | Need description, metadata, and formal definition (source) for a theorem ID; refuses to run until the first-run gate passes. |
| Download & scaffold | `python3 scripts/download_theorem.py [--config <path>] <id> [--output-dir <path>] [--force]` | Creating a local Lean or Rocq proof workspace after the first-run gate passes. |

`openmath_api.py` is the shared API client. `openmath_env_config.py` reads shared user preferences from `openmath-env.json`.

### Notes

- **Endpoints**: Default website is `https://openmath.shentu.org`; default API host is `https://openmath-be.shentu.org`. Runtime overrides: `OPENMATH_SITE_URL`, `OPENMATH_API_HOST`.
- **Language**: User-facing and API language naming is `rocq`.
- **No fallback**: If `preferred_language` is `lean`, query only Lean by default. If no theorems are found, report that result and stop; do not automatically query Rocq, and vice versa.
- **Lean scaffold**: Pins Lean and mathlib4 to `v4.28.0`. Rocq scaffold is `_CoqProject`-based.
- **After download**: Use the `openmath-lean-theorem` skill for Lean environment setup, preflight, external skill installation, and the proving workflow.

## References

Load when needed (one level from this file):

- **[references/init-setup.md](references/init-setup.md)** — Discovery-first setup flow for shared `openmath-env.json`, preferred language, and config visibility.
- **[references/reward_overview.md](references/reward_overview.md)** — How rewards are calculated and how to claim them.
