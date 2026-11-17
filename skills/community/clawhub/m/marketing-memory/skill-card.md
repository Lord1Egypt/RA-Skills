## Description:

Gives agents persistent marketing memory for storing, recalling, and searching campaign history and results using BlueColumn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and agents use this skill to recall prior campaign performance before a new interaction and store summarized campaign notes afterward. It is intended for workflows that need searchable campaign memory through BlueColumn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign discussions may include confidential plans, customer data, personal data, metrics, or secrets before being written to external persistent memory.

Mitigation: Use the skill only with approval for what may be stored, redact sensitive details before writes, and confirm BlueColumn retention, deletion, access, and key-rotation practices.

Risk: Persistent recall can surface outdated or inappropriate campaign context in later agent interactions.

Mitigation: Review recalled memory before relying on it and delete or correct records that are no longer valid.

## Reference(s):

- [BlueColumn API reference](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/marketing-memory)
- [Publisher profile](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends memory requests to the BlueColumn-backed API endpoints described by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
