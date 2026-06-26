# Docs Source of Truth

## Shared Docs Rule
The following files must stay synchronized between:
- `/opt/lmail/lmail-docs`
- `/opt/lmail/apps/dashboard/public/lmail-docs`

Shared files:
- `AGENT_HANDOFF_PROMPT.md`
- `AGENT_QUICKSTART.md`
- `AGENT_TOOLS.json`
- `AGENT_SPEC.json`
- `AGENT_DOCS_INDEX.md`

## Governance Steps
1. Edit docs in your chosen source location.
2. Mirror changes to the second location.
3. Run `scripts/sync_docs_check.sh`.
4. Re-run smoke flows if registration contract changed.

## Contract-Sensitive Changes
When auth or registration endpoints change, always update:
- request fields
- error codes
- startup sequence
- tool definitions
