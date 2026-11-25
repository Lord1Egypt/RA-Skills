## Description:

Imports user-selected NotebookLM notes into a personal knowledge wiki on demand or on a schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-wei](https://clawhub.ai/user/samuel-wei)

### License/Terms of Use:

MIT-0

## Use Case:

HiJavis users use this skill to bring selected NotebookLM text notes into their personal knowledge wiki, either on demand or on a chosen schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security assessment is suspicious with medium confidence because inspection covered only 8 of 22 components and static analysis was degraded for some files.

Mitigation: Review the complete artifact and its permissions before installation; the available scan is incomplete and is not a finding of malicious intent.

Risk: The skill sends selected note content through an authenticated push and can run on a configured schedule.

Mitigation: Select notebooks deliberately, review the destination and schedule, and use the dry-run preview before a push.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/samuel-wei/skills/notebooklm-ingest)
- [HiJavis app listing](https://apps.apple.com/us/app/hijavis/id6745134765)
- [Credential contract](references/credential-contract.md)
- [Trigger contract](references/trigger-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [JSON command results and Markdown chat summaries or history]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Run results and local ingest history; note text is sent to the wiki only through the configured push flow.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
