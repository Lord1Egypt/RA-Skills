## Description:

Access and manage NocoDB databases via REST APIs, covering bases, tables, fields, records, links, filters, sorts, attachments, and Enterprise workspace, view, script, team, and collaboration APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkphoenix2704](https://clawhub.ai/user/darkphoenix2704)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure NocoDB API access and manage NocoDB workspaces, bases, tables, fields, records, permissions, attachments, and API tokens through an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make real database, permission, attachment, and API-token changes in NocoDB.

Mitigation: Use a least-privilege NocoDB token and review proposed create, update, delete, collaboration, and token commands before execution.

Risk: Commands that use names or IDs can affect the wrong workspace, base, table, field, view, record, or token if the target is mistaken.

Mitigation: Verify target IDs before destructive commands and enable NOCODB_VERBOSE when resolving names to IDs.

Risk: Attachment upload commands send local files to the configured NocoDB server.

Mitigation: Upload only files intended for that NocoDB server and confirm the server URL before running upload commands.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/darkphoenix2704/skills/nocodb-official)
- [ClawHub publisher profile](https://clawhub.ai/user/darkphoenix2704)
- [Agent Skills Open Standard](https://agentskills.io)
- [NocoDB Cloud](https://app.nocodb.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses NOCODB_TOKEN, NOCODB_URL, NOCODB_VERBOSE, curl, and jq.]

## Skill Version(s):

0.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
