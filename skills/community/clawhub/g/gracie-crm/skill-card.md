## Description:

Manage and track Gracie AI Receptionist sales leads with CLI commands to add leads, update statuses, log calls and notes, and review follow-ups and pipeline summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayjjimenez](https://clawhub.ai/user/jayjjimenez)

### License/Terms of Use:


## Use Case:

Sales operators and agents use this skill to maintain a local CRM for Gracie AI Receptionist prospects, including adding leads, recording call outcomes, scheduling follow-ups, and checking pipeline status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships live-looking CRM contact records and notes in crm.json.

Mitigation: Review or remove bundled CRM records before installation or redistribution, and store active CRM data in a private location with restrictive permissions.

Risk: The import command may read leads from a fixed private MASTER_LEAD_LIST.md path under the user's home directory when that file exists.

Mitigation: Run import only after confirming that source file is intended for this CRM, or remove or modify the import behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayjjimenez/skills/gracie-crm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration]

**Output Format:** [Markdown guidance with inline shell commands and local CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads a local JSON CRM data file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
