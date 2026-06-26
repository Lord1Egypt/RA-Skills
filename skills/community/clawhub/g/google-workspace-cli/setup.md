# Setup - Google Workspace CLI

Read this when `~/google-workspace-cli/` is missing or empty.
Keep onboarding lightweight and task-first.

## Operating Priorities

- Answer the immediate request first, then improve future execution.
- Confirm when this skill should auto-activate for Workspace CLI tasks.
- Establish read-only, dry-run, or apply boundaries before any mutation.
- Keep one account and one tenant scope per operation batch.

## First Activation Flow

1. Confirm integration behavior early:
- activate automatically for `gws` and Google Workspace API tasks or explicit-only
- proactive suggestions allowed or not
- hard no-go scenarios

2. Confirm operational context:
- individual productivity workflows
- team operations and reporting
- admin and compliance workloads

3. Confirm risk boundaries:
- dry-run required for all writes or only high-impact writes
- confirmation token required for send/share/delete operations
- production restrictions vs test tenant availability

4. Initialize local workspace if approved:
```bash
mkdir -p ~/google-workspace-cli
touch ~/google-workspace-cli/{memory.md,command-log.md,change-control.md,incidents.md,mcp-profiles.md}
chmod 700 ~/google-workspace-cli
chmod 600 ~/google-workspace-cli/{memory.md,command-log.md,change-control.md,incidents.md,mcp-profiles.md}
```

5. If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Default to inspect mode, then dry-run, then apply.
- Prefer minimal scopes and explicit account routing.
- Keep command templates reusable with placeholders for ids.
- Track each mutating command with rationale and rollback notes.

## What to Save

- activation preferences and never-run boundaries
- default account and fallback account policy
- approved scope profiles by workflow type
- known-good command templates and failure signatures
- unresolved risks and mitigation decisions

## Guardrails

- Never ask users to paste credentials in chat.
- Never imply write safety without id resolution and preview.
- Never bypass tenant policy or OAuth verification requirements.
