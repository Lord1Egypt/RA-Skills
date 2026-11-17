## Description:

Journal Memory helps agents store, recall, and search journal entries through BlueColumn persistent memory using a BlueColumn API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent keep a persistent, searchable journal memory and retrieve prior entries for context. It requires a BlueColumn API key and sends journal text or interaction summaries to BlueColumn/Supabase endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages storing and recalling potentially sensitive journal entries and conversation summaries in remote BlueColumn/Supabase memory without clear consent or minimization controls.

Mitigation: Require per-entry approval, review the exact payload before sending, avoid secrets and regulated personal data, and confirm how stored memories can be inspected, deleted, and separated from trusted instructions.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [Journal Memory ClawHub release](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/journal-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API payload examples for storing notes, quick notes, and recalling journal entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
