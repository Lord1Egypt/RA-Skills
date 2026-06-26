---
name: nebula-claw-developer
description: Provision, inspect, and terminate disposable OpenNebula virtual machines through a restricted control plane API. Use when an OpenClaw agent needs a short-lived VM for development, debugging, integration testing, package installation, or risky experiments that should run in isolation instead of on the main host.
---

# Nebula Claw Developer

Use the restricted OpenNebula control plane API to create, list, and terminate disposable virtual machines for isolated work.

## Workflow

1. Read `references/api.md` for the API contract and request examples.
2. Check API health before taking action.
3. List visible VMs and reuse an existing one only if it clearly matches the task.
4. Prefer curated template names over numeric identifiers and use the configured template catalog descriptions to choose the right one.
5. Create a fresh VM when isolation matters more than reuse.
6. Record the VM name and guest IP in output when available so later access and cleanup are obvious.
7. Terminate the VM when the task is complete unless the user explicitly asks to keep it.

## Safety constraints

- Use only curated templates, images, and networks intentionally shared with the restricted OpenNebula user.
- Do not switch to broad administrative OpenNebula privileges for routine work.
- Do not assume arbitrary templates are safe to instantiate.
- Treat created VMs as disposable unless the user asks for persistence.
- If the API health check fails, stop and diagnose before attempting create or delete operations.

## Naming guidance

Use short task-based names that make later cleanup obvious.

Recommended pattern:

- `<purpose>-<project>-<short-date>`

Examples:

- `test-nebula-api-2026-04-10`
- `build-myapp-2026-04-10`
- `repro-login-bug-2026-04-10`

## Bundled resources

- Read `references/api.md` for endpoints, payloads, and example responses.
- Read `references/setup.md` when you need the OpenNebula-side restricted-user and curated-resource setup pattern.
- Use `scripts/vm_api.sh` for deterministic health, list, create, and delete calls against the restricted API.

## Output expectations

When using this skill, report:

- the API endpoint used
- the VM name
- the template name
- the guest IP when the API exposes it
- the result of create, list, or delete operations
- whether the VM was left running or destroyed

## Source 

See more the source code and more documentation on [GitHub](https://github.com/ktfh-claw/nebula-claw-developer)
