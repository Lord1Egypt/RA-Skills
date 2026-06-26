# What counts as material?

Use this threshold before opening a governance PR or running Workflow C (ship).

## Requires governance PR (material)

- OpenClaw **system updates**: runtime, gateway, package install, service/systemd changes
- **Cron** create/remove/schedule/payload change
- **Plugin** install, remove, or update affecting automation
- **Workflow behavior** change after a confirmed working update
- **Runbook** create or substantive edit under `workflows/runbooks/`
- **Registry** new workflow or material edit to triggers, owners, RACI, status promotion
- **Cross-repo script path** referenced by cron, systemd, or `tools_or_scripts`
- Shared-agent config affecting **routing, tools, or recall**
- Anything you would need to **restore from git** after disk loss

## Usually does NOT require governance PR

- Read-only `discover`, `check`, `regen --check`, `doctor` (Workflow A)
- Local agent notes in workspace `memory/` (not governance root)
- Fixing typos in runbook **draft** on a feature branch before human review (still ship if merged)
- Inventory refresh (`discover --inventory`) with no registry semantic change and no promotion

## Gray area — ask the human

- README-only wording that does not change verification gates
- Promoting `discovered` → `active` without runbook body filled in yet
- Changes that trigger **external smoke tests** (see SKILL.md verification section)

When in doubt, treat as material. Silent drift is harder to fix than an extra governance PR.
