## Description:

Procedural Memory helps an agent identify successful recurring workflows and save them as reusable skill files for future conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjin113](https://clawhub.ai/user/chenjin113)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture successful multi-step workflows as reusable skills, with optional review triggers after repeated success, complex task completion, or end-of-day reflection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived workflows may be saved into persistent skill files or logs, including sensitive references from user conversations.

Mitigation: Require explicit approval and preview before each new skill or log entry, avoid sensitive conversations while active, and define deletion and redaction rules for stored memories.

Risk: The autonomous-operation SOP permits maintenance, backups, scanning, and local write activity after user inactivity.

Mitigation: Remove or disable the autonomous-operation SOP before use unless autonomous maintenance is intended and bounded by local policy.

## Reference(s):

- [Autonomous Operation SOP](autonomous-operation-sop.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown skill files, markdown logs, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent skill and log files in user-scoped directories.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
