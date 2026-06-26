GPU CLI ClawHub Skill (Stable)

Safely run local `gpu` commands from OpenClaw/ClawHub agents with guardrails (dry-run preview, command whitelist, budget/time caps, and clear remediation), without modifying GPU CLI itself.

Files
- `SKILL.md` - ClawHub skill metadata, permissions, and usage instructions.
- `manifest.yaml` - ClawHub manifest (permissions, triggers, settings).
- `runner.sh` - Execution wrapper with guardrails.
- `selftest.sh` - Hermetic tests using `tools/mock-gpu/` (no real gpu binary needed).
- `templates/prompts.md` - Curated prompts for common tasks.

Quick usage (from an agent)
- Trigger: "/gpu" or phrases like "Use GPU CLI to ..." (as configured on ClawHub)
- Example: "Use GPU CLI to run gpu status --json"

Notes for publishers
- Mark channel as Stable, add logo/screenshots/demo.
- Keep permissions minimal: Bash + Read, workspace-scoped; network off for the skill itself.
- Bump version in the ClawHub publish form (current: 1.1.1).
- Upload this folder (not a zip).
