## Description:

Connect to NocoDB databases via REST API v3 to query records, manage database structure, handle linked records, apply filters and sorts, and upload attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dofbi](https://clawhub.ai/user/dofbi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent work with NocoDB Cloud or self-hosted NocoDB instances through the REST API. It supports database record workflows, schema changes, linked records, attachments, collaboration administration, and token-related operations according to the user's NocoDB plan and token permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad NocoDB data, schema, membership, token, script, deletion, and file-upload actions when given a powerful API token.

Mitigation: Use a least-privilege token, test in a non-production workspace first, and require explicit human approval before delete, schema, token, team, membership, script, or file-upload actions.

Risk: The required NOCODB_TOKEN can expose database access if printed, logged, or shared.

Mitigation: Store the token as an environment secret, avoid echoing it, and rotate it if it appears in logs or chat history.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dofbi/skills/nocodb-api)
- [NocoDB Documentation](https://docs.nocodb.com/)
- [NocoDB REST API Reference](https://docs.nocodb.com/developer-resources/rest-APIs/)
- [NocoDB Website](https://nocodb.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON API responses from NocoDB commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOCODB_TOKEN, optionally NOCODB_URL, and local curl and jq binaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
