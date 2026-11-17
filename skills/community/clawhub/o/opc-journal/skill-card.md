## Description:

OPC Journal is a local-only CLI-style skill for One Person Company growth tracking that records entries and tasks, searches or exports journal history, and prepares raw pattern, milestone, and insight context for caller interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coidea](https://clawhub.ai/user/coidea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use OPC Journal to maintain a local One Person Company growth journal, record entries and tasks, search or export history, and prepare raw pattern, milestone, and insight context for the caller to interpret.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export command can write outside the promised customer folder and overwrite arbitrary user-writable files.

Mitigation: Review before installing, keep exports inside ~/.openclaw/customers/{customer_id}/, and do not allow untrusted prompts to choose export paths.

Risk: Journal and task data persists locally until archived or cleared.

Mitigation: Set retention expectations before use and archive or clear local data when it is no longer needed.

Risk: Deletion by incomplete entry IDs can remove unintended journal content.

Mitigation: Use complete entry IDs for delete operations and keep the existing --force confirmation requirement.

## Reference(s):

- [ClawHub OPC Journal skill page](https://clawhub.ai/coidea/skills/opc-journal)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [JSON command results with optional Markdown or JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only file persistence under ~/.openclaw/customers/{customer_id}/; destructive delete and archive clearing require --force.]

## Skill Version(s):

2.5.2 (source: server release evidence and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
