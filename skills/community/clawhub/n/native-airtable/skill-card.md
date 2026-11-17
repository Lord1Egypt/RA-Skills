## Description:

Read Airtable bases, tables, and records directly via the Airtable API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeninja23](https://clawhub.ai/user/codeninja23)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect Airtable bases, tables, and records through Airtable's official API when they need spreadsheet or database content during a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Airtable Personal Access Token and command output can include Airtable record contents.

Mitigation: Use a read-only token scoped only to the bases the agent needs to access.

Risk: Broad token access can expose more Airtable data than the task requires.

Mitigation: Limit token permissions to data.records:read and schema.bases:read, and restrict base access during token creation.

## Reference(s):

- [Native Airtable on ClawHub](https://clawhub.ai/codeninja23/skills/native-airtable)
- [Airtable Personal Access Tokens](https://airtable.com/create/tokens)
- [Airtable API](https://api.airtable.com/v0)
- [Airtable Metadata API](https://api.airtable.com/v0/meta)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AIRTABLE_PAT and can print Airtable base, table, and record contents returned by Airtable.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
