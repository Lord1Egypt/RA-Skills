## Description:

SQLite long-term memory compression system for extended memory life. Adds tools for agents to control their memory functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danavfrost](https://clawhub.ai/user/danavfrost)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to persist durable preferences, facts, corrections, and project context across agent sessions, then surface relevant memories through MCP tools and bootstrap context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compression reads full OpenClaw session transcripts and may pass excerpts through the configured model provider.

Mitigation: Install only when transcript processing is acceptable; avoid entering secrets in sessions that may be compressed and review extracted memories regularly.

Risk: Default automation can overwrite older session transcripts after memories are confirmed.

Mitigation: Use `--no-wipe` or skip the cron setup unless transcript replacement is explicitly desired.

Risk: Selected memories and the bootstrap cache are stored in plaintext and injected into future sessions.

Mitigation: Keep the memory directory access-restricted and delete or edit memories that should not persist.

Risk: The setup flow registers persistent MCP, hook, and scheduled compression components.

Mitigation: Run the uninstall script or remove the registered OpenClaw components when ongoing memory access is no longer needed.

## Reference(s):

- [OpenMem Database Schema](references/schema.md)
- [OpenMem ClawHub Release](https://clawhub.ai/danavfrost/skills/openmem)
- [OpenAuto Integration](https://clawhub.ai/halthelobster/openauto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown bootstrap context, JSON MCP tool responses, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores selected memories locally in SQLite and writes a plaintext cache used for bootstrap injection.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact version references)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
