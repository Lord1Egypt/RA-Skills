## Description:

Sets up or standardizes an OpenClaw workspace using the Fire Dragon Fruit Architecture, with one strong main agent, an isolated rescue agent, layered file memory, project truth documents, heartbeat, isolated cron, official Feishu integration, Ollama memory embeddings, and a durable long-running operating model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staiv1](https://clawhub.ai/user/staiv1)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to convert a fresh or existing OpenClaw setup into a persistent operating workspace with durable memory, project files, scheduled maintenance, and controlled integrations. It is intended for system-level workspace setup rather than small prompt edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make lasting changes to agent instructions, memory workflows, project files, heartbeat, and cron.

Mitigation: Require an explicit file-by-file plan, review proposed changes before applying them, and keep backups before installation.

Risk: Scheduled reflection or maintenance could apply memory or instruction changes without enough oversight.

Mitigation: Configure scheduled reflection to produce proposed diffs for review rather than automatically applying memory or instruction changes.

Risk: Implicit invocation could trigger broad workspace restructuring when a narrower task was intended.

Mitigation: Disable implicit invocation when possible and use the skill only for intentional system-level OpenClaw setup or normalization.

## Reference(s):

- [Fire Dragon Fruit Architecture](references/fire-dragon-fruit-architecture.md)
- [Architecture](references/architecture.md)
- [Checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file edits, configuration steps, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace files, memory files, project documents, skills, heartbeat guidance, cron configuration, and integration settings.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
