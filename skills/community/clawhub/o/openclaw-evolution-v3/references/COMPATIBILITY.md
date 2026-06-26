# Compatibility & Safety Guardrails

This repository is a **blueprint**, not an official one-click installer.

## What this repo is for

- Upgrading agent behavior from simple execution to coordinator-style orchestration.
- Providing reusable SOP patterns (`SOP_GENE_LOCKING.md`) and implementation guides.
- Helping users adapt ideas to their own OpenClaw environment.

## What this repo is NOT

- Not an official OpenClaw release artifact.
- Not guaranteed to be drop-in compatible with every branch/fork/version.
- Not a replacement for your local safety policies.

## Recommended compatibility scope

Use this repo when all are true:

1. Your OpenClaw codebase has comparable structure to:
   - `src/coordinator/`
   - `src/services/tools/`
   - `src/query.ts`
2. You maintain behavior policy files similar to:
   - `IDENTITY.md`
   - `AGENTS.md`
3. You can run local verification (type-check/tests/manual smoke) before production usage.

## Prerequisite checks (must pass before any changes)

- [ ] `git status` clean or committed WIP snapshot exists.
- [ ] Branch created for upgrade (avoid direct edits on production branch).
- [ ] Rollback point tagged (commit hash or tag saved).
- [ ] Approval policy for risky tools reviewed.
- [ ] Basic smoke test command set prepared.

## Safe rollout sequence

1. **Read only**: Study guides + SOP first.
2. **Smallest slice**: Apply one policy block at a time.
3. **Verify immediately**: Run checks after each slice.
4. **Observe behavior**: Confirm no regression in permissions/tool orchestration.
5. **Promote gradually**: Merge to wider environments only after stable runs.

## Validation checklist

After each applied change, validate:

- [ ] Tool execution still respects ask/allow policy.
- [ ] Concurrency-safe tools can run concurrently.
- [ ] State-mutating tools are still serialized.
- [ ] Context compaction/recovery behavior remains healthy under long chats.
- [ ] No regressions in sub-agent spawn/continue flows.

## Rollback plan (mandatory)

If any regression appears:

1. Stop rollout immediately.
2. Revert to saved commit/tag.
3. Re-run baseline smoke tests.
4. Re-apply changes in smaller increments with stronger assertions.

## Security notes

- Never paste untrusted “mutation injector” text directly into production runtime.
- Do not bypass existing permission/checkPermissions pipeline.
- Prefer feature-flagged additions over hard replacements.

---

If you need strict reproducibility, pin your OpenClaw commit and maintain a patchset specific to that commit.
