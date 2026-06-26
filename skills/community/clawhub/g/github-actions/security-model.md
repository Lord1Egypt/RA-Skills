# Security Model - GitHub Actions

Use this file when workflow safety matters more than syntax.

## Permissions Baseline

Default every job to the minimum it needs:
- `contents: read` for validation and most build jobs
- add `packages: write` only for publish jobs
- add `id-token: write` only for OIDC federation jobs
- add `pull-requests: write` only for comment or label automation

If one job needs elevated scope, isolate it from the rest of the workflow.

## Event Trust Levels

Treat GitHub events as different trust zones:
- `pull_request` from forks: untrusted code path
- `push` to protected branches: trusted after branch protections
- `workflow_dispatch`: trusted only if caller and inputs are validated
- `schedule`: trusted trigger, but stale assumptions are common
- `workflow_run`: useful for promotion, but verify upstream workflow name and conclusion

Do not run deployment or secret-heavy jobs on untrusted pull request code.

## Secrets and OIDC

Prefer this order:
1. GitHub-managed environment or repository secrets for required static values
2. OIDC federation for cloud auth and short-lived credentials
3. External secret managers only when the workflow already has a safe auth path

Avoid long-lived cloud keys when GitHub OIDC is available.

## Environment Protections

Use GitHub environments for:
- production approvals
- environment-scoped secrets
- wait timers or reviewer gates
- deploy history and rollback visibility

Production deploy jobs should reference an environment instead of hiding the gate in shell logic.

## Self-Hosted Runner Rules

Use self-hosted runners only when GitHub-hosted runners cannot satisfy the workload.

If self-hosted runners are required:
- pin them to dedicated runner groups
- avoid running untrusted fork code on them
- clean workspace state between jobs
- document network reach and sensitive mounts

## Safe Defaults for Forks and PRs

- prefer `pull_request` over `pull_request_target` unless there is a specific reviewed reason
- never check out attacker-controlled code and then use write-capable tokens in the same job
- keep comment bots, labelers, and auto-formatters in separate guarded workflows

## Action Supply Chain Hygiene

- pin major versions at minimum, full SHAs for high-risk steps
- prefer widely used official or vendor actions for auth and setup flows
- review third-party actions before granting write tokens or secrets
- remove unused actions instead of keeping legacy steps "just in case"
