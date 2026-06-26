# Debugging Playbook - GitHub Actions

Use this file after a workflow fails or behaves inconsistently.

## Failure Classification

Sort the failure before editing YAML:

| Failure class | Typical symptoms | First check |
|---------------|------------------|-------------|
| Trigger mismatch | Workflow did not start | event, branch, path filters, `if:` conditions |
| Toolchain drift | Works locally, fails in CI | runner image, setup action version, lockfile |
| Permission denial | 403, auth, cloud reject | `permissions:`, environment gate, token source |
| Contract break | Missing file, empty artifact, wrong path | artifact names, working directory, outputs |
| External flake | network, registry, API timeout | retries, provider status, rate limits |

## First Actions

1. Open the failed run and identify the first wrong step, not the loudest later step.
2. Compare the failing event, ref, and actor with the expected workflow contract.
3. Check whether the failure is deterministic or only appears on some runs or matrix cells.
4. Download artifacts or summaries before re-running anything.

## Useful `gh` Commands

If `gh` is available, these commands shorten investigation:

```bash
gh run list --limit 10
gh run view <run-id> --log-failed
gh run download <run-id> -D /tmp/gha-run
gh workflow view <workflow-name>
```

## Reproduction Strategy

Reproduce only the failing surface:
- shell logic -> run the same commands locally or in a dev container
- missing environment variable -> inspect workflow inputs and environment source
- matrix-specific issue -> reproduce that one runtime or OS target
- action behavior -> check action version, inputs, and upstream release notes

`act` can help reproduce shell behavior and basic workflow flow, but it is not a perfect GitHub-hosted runner clone.

## High-Signal Debug Artifacts

Prefer adding temporary diagnostics that are easy to remove:
- `echo` stable context like branch, actor, matrix cell, or path
- write small summaries to `$GITHUB_STEP_SUMMARY`
- upload generated manifests or test reports as artifacts
- print resolved paths before using them

Avoid dumping secret-heavy environments or huge recursive directory listings.

## When to Change the Workflow

Edit the workflow only after you can explain one of these:
- wrong trigger or condition
- wrong permission or credential path
- wrong file or artifact contract
- wrong runner assumption
- wrong cache key or dependency restore behavior

If the cause is still unclear, add diagnostics first and keep the workflow shape stable.
