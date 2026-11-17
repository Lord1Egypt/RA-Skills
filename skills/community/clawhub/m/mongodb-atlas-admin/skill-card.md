## Description:

Browse MongoDB Atlas Admin API specifications and execute operations when credentials are provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finishy1995](https://clawhub.ai/user/finishy1995)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to browse MongoDB Atlas Admin API operations, inspect schemas, and prepare or execute Atlas API calls with configured service account credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Atlas Admin API authority from configured service account credentials.

Mitigation: Use a least-privilege Atlas service account and review requested operations before enabling live API calls.

Risk: ATLAS_API_BASE_URL can redirect credential and API requests to a configurable host.

Mitigation: Leave ATLAS_API_BASE_URL unset or set it only to https://cloud.mongodb.com.

Risk: Access tokens are cached locally in plaintext.

Mitigation: Treat the local token cache as sensitive credential material and clear it when no longer needed.

Risk: State-changing Atlas operations can modify or delete resources.

Mitigation: Use dry-run previews first and execute state-changing calls only after explicit user approval.

## Reference(s):

- [MongoDB Atlas Admin API documentation](https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/)
- [MongoDB Atlas skill release](https://clawhub.ai/finishy1995/skills/mongodb-atlas-admin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce dry-run previews and JSON API responses when live Atlas calls are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
