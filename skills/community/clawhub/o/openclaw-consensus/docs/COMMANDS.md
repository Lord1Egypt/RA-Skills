# Commands

## Runtime commands that exist now

### Show help
```bash
node src/cli.mjs help
```

### List configured API-backed models from the active OpenClaw workspace config
```bash
node src/cli.mjs models
```

### Run one 2-round consensus flow
```bash
node src/cli.mjs run \
  --brief "<brief>" \
  --models "openai-codex/gpt-5.4,openai-codex/gpt-5.5" \
  --orchestrator-model "openai-codex/gpt-5.4" \
  --label "optional-label"
```

### Run from a brief file
```bash
node src/cli.mjs run \
  --brief-file ./path/to/brief.md \
  --models "openai-codex/gpt-5.4,openai-codex/gpt-5.5"
```

## Local skill lifecycle commands

### Install the repo as a workspace skill
```bash
./scripts/install-skill.sh
```

### Uninstall the workspace skill link
```bash
./scripts/uninstall-skill.sh
```

### Verify the skill is visible to OpenClaw
```bash
openclaw skills info openclaw-consensus
```

## Validation commands used in this repo

### Happy-path validation
```bash
node src/cli.mjs run \
  --brief-file validation/2026-04-29/brief-happy-path.md \
  --models "openai-codex/gpt-5.4,openai-codex/gpt-5.5" \
  --orchestrator-model "openai-codex/gpt-5.4" \
  --label "validation-happy-path"
```

### Failure-path validation
```bash
node src/cli.mjs run \
  --brief-file validation/2026-04-29/brief-failure-path.md \
  --models "openai-codex/gpt-5.4,anthropic/claude-sonnet-4-6" \
  --orchestrator-model "openai-codex/gpt-5.4" \
  --label "validation-fallback-failure"
```

## Important command-surface rules
- The MVP requires an explicit model shortlist.
- The repo rejects `ollama/*` models.
- The repo rejects configured-model fallback: if OpenClaw runs a different model than requested, the run fails and preserves artifacts.
- `run.json` records whether the orchestrator model was explicit or defaulted from the workspace agent primary model.
- `run` rejects unknown flags (e.g. typos like `--orchestator-model`) instead of silently ignoring them.
- `run` accepts `--model-timeout-ms <ms>` to bound each model call (default 5 minutes).
- `run` rejects `--run-root` paths inside common system directories or pointing at non-empty directories.

## Offline regression tests
All tests below are deterministic, do not invoke `openclaw`, and do not call
any provider. They are safe to run on every change; they do not consume API
credit.

### Run the full offline suite
```bash
./scripts/run-tests.sh
# or
npm test
```

### Run individual files
```bash
# Pure-helper self-checks (parseFlags, validateExplicitRunRoot, parseTimeoutMs,
# prompt nonces, sanitizeErrorForPersistence, slugify, safeModelName, etc.)
node validation/tests/cli-helpers.test.mjs

# Extended helper coverage (createRunDir collision-safety + run-root rejection,
# getConfiguredApiModels filtering/sorting, prompt structural contract,
# sanitizeErrorForPersistence edge cases, parseFlags edge cases).
node validation/tests/cli-extended.test.mjs

# CLI-boundary tests via spawnSync. These exercise the real cli.mjs entrypoint
# but only along paths that fail before any openclaw subprocess is spawned
# (unknown flag, duplicate flag, bad --model-timeout-ms, forbidden --run-root).
node validation/tests/cli-cli.test.mjs
```

## Optional live checks
End-to-end live runs cost API credit. They are not run by `npm test` and must
be invoked explicitly. See the validation commands above
(`Happy-path validation`, `Failure-path validation`) for the sanctioned
manual flows.
