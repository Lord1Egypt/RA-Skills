# AGENTS.md — Codex CLI Runbook for NanoGPT Plugin

Living document for Codex CLI + human contributors. Keep this updated when behavior, workflows, or constraints change.

## Project Overview

- Package: `@openclaw/nano-gpt`
- Provider ID: `nano-gpt`
- Type: OpenClaw provider plugin
- Purpose: NanoGPT support in OpenClaw with API-key auth, dynamic model catalog, and usage/balance tracking
- Repository: `http://git.search.dontexist.com/openclaw/nano-gpt-plugin`

## Repository Map

- `AGENTS.md`: operational guide for Codex/humans
- `PLAN.md`: planning and replanning notes
- `README.md`: user-facing setup/usage documentation
- `openclaw.plugin.json`: plugin metadata and auth config
- `package.json`: scripts + package metadata
- `src/provider.ts`: provider entry/registration logic
- `src/catalog.ts`: NanoGPT model catalog client + mapping
- `src/usage.ts`: usage and balance clients
- `src/types.ts`: API response/request types
- `tests/provider.test.ts`: provider unit tests
- `test_results/<YYYY-MM-DD>/`: integration test artifacts


## Commit and PR Conventions

### Commit format

- Subject prefixes: `feat:`, `fix:`, `test:`, `docs:`, `chore:`
- Keep subject line under ~72 chars when possible.

Commit subject template:

```text
<type>: <concise change summary>
```

Commit body template (use when not trivial):

```text
Why:
- <problem or requirement>

What changed:
- <change 1>
- <change 2>

Validation:
- `pnpm test`
- `pnpm test -- tests/`
- `openclaw plugins inspect nano-gpt`
- integration artifacts: `test_results/<YYYY-MM-DD>/`
```

Example commit:

```text
fix: wire nano-gpt onboard and model-set integration commands

Why:
- Integration runbook had placeholders for onboarding and model selection.

What changed:
- Added concrete `openclaw onboard --nano-gpt-api-key` command.
- Added `openclaw models set nano-gpt/...` default model step.

Validation:
- Reviewed AGENTS command template block.
```

### Pull request expectations

PR body template:

```markdown
## Summary
- <behavior change 1>
- <behavior change 2>

## Risk / Rollback
- Risk: <low|medium|high>
- Rollback: <how to revert safely>

## Validation
- [ ] `pnpm test`
- [ ] `pnpm test -- tests/`
- [ ] Integration run completed
- Artifacts: `test_results/<YYYY-MM-DD>/`

## Docs Updated
- [ ] `AGENTS.md`
- [ ] `PLAN.md`
- [ ] `README.md`
```

PR title template:

```text
<type>: <short change summary>
```

Always link integration artifact paths when integration was run, e.g. `test_results/<YYYY-MM-DD>/`.
## Required Decisions (Do Not Drift)

- Base URL: `https://nano-gpt.com/api/v1`
- API mode: `openai-completions`
- Auth: `NANOGPT_API_KEY` via onboarding flow only (not read directly from env)
- Catalog behavior: dynamic fetch, cache per session
- Dynamic model resolution: enabled (`resolveDynamicModel`)
- Usage endpoints: `fetchUsageSnapshot` + `fetchBalance`

## Behavior + Mapping Rules

- NanoGPT model IDs may include slashes; pass model IDs through unchanged.
- Map pricing from dollars-per-million-token to dollars-per-token:
  - `inputCostPerToken = pricing.prompt / 1_000_000`
  - `outputCostPerToken = pricing.completion / 1_000_000`
- Map `vision: true` to `input: ["text", "image"]`.
- Map `reasoning: true` to `reasoning: true`.
- Do not refetch catalog on every inference call; fetch lazily and cache.
- Include `include_usage: true` in extra params.
- Known runtime behavior: message-level usage may be zero; canonical usage comes from usage snapshot endpoint.

## Unit Test Location and Workflow

### Where unit tests live

- `tests/provider.test.ts`
- Any new unit tests should be added under `tests/` with `*.test.ts` naming.

### How to run unit tests

```bash
pnpm test
pnpm test -- tests/
```

### Unit test conventions

- Use Vitest (`describe`, `it`, `expect`, `vi`).
- Mock runtime with `createPluginRuntimeStore` and cast to `PluginRuntime`.
- Prefer async mocks via `vi.fn().mockResolvedValue(...)`.
- No live OpenClaw instance required.

## Integration Test

Use `final_integration_test.sh` to run integration tests and collect data.

To verify `include_usage: true` is being added correctly, check that `totalTokens > 0` in collected session `*.jsonl` files.

## Research Docs Location

Research and design notes live in `docs/`:

- `docs/00-research-notes.md`
- `docs/01-nano-gpt-intro.md`
- `docs/02-nano-gpt-auth.md`
- `docs/03-nano-gpt-models-api.md`
- `docs/04-nano-gpt-usage-api.md`
- `docs/05-openclaw-provider-sdk.md`
- `docs/06-openclaw-existing-integration.md`

## Codex Memory Items

Codex memory directory on this machine:

- `/home/node/.codex/memories`

Current known state:

- Directory exists
- No memory files detected yet

When memory files are added, maintain a short index here:

- `<absolute-memory-file-path>`: `<one-line summary>`

## OpenClaw SDK References

- `/app/docs/plugins/sdk-provider-plugins.md`
- `/app/docs/plugins/sdk-testing.md`

Key imports:

```ts
import { defineSingleProviderPluginEntry } from "openclaw/plugin-sdk/provider-entry";
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
import type { PluginRuntime } from "openclaw/plugin-sdk/runtime-store";
```

## Replanning Workflow (README-Feature Driven)

When replanning, use `README.md` `## Features` as the baseline checklist.
Every replan in `PLAN.md` should explicitly map tasks to these features:

- Dynamic model catalog from `https://nano-gpt.com/api/v1/models?detailed=true`
- Auto-populate model capabilities (vision, reasoning, context window, pricing)
- `NANOGPT_API_KEY` handling
- `openclaw onboard --nano-gpt-api-key <key>` flow
- Include `include_usage: true` on outgoing requests
- Subscription usage tracking via `/api/subscription/v1/usage`
- Balance checking via `/api/check-balance`
- Support broad NanoGPT model families (OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, Qwen, Groq, and others)

### Replan steps

1. Read current `README.md` features and copy them into a checklist block in `PLAN.md`.
2. Mark each feature as one of: `implemented`, `partial`, `not started`, `needs verification`.
3. Create tasks grouped by feature, with test coverage expectations per task.
4. Identify integration-test evidence needed for each changed feature.
5. After implementation, update:
   - `PLAN.md` status per feature
   - `README.md` features if behavior changed
   - `AGENTS.md` gotchas/workflow if process changed

## Maintenance Checklist

- Keep this file and `PLAN.md` aligned after each major change.
- Add newly discovered gotchas immediately.
- Keep integration procedure accurate and date-stamped where useful.
- Ensure every integration run has artifacts in `test_results/<YYYY-MM-DD>/`.
- If project-level memory files are created, add them to the memory index section above.

## Standard Update Procedure

When making changes that pass integration tests:

1. **Run unit tests**: `pnpm test`
2. **Run integration test**: `bash final_integration_test.sh`
3. **Update version**: Bump `version` in `package.json` (semver patch for bug fixes, minor for features)
4. **Commit**: `git add -A && git commit -m "<type>: <change summary>"`
5. **Push**: `git push`
6. **Publish to clawhub**: `npx clawhub publish <plugin-dir>` (requires `clawhub login` first)

Version format: `0.1.x` for development releases.

### Integration test artifacts

After running `final_integration_test.sh`, artifacts are saved to `test_results/<YYYY-MM-DD>/`:
- `gateway.log` — gateway service logs
- `*.jsonl` — session transcripts with usage data

Check that `totalTokens > 0` in session files to verify `include_usage: true` is working.
