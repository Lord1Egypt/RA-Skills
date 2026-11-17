## Description:

Manage HumanPost social accounts, prepare content drafts, queue approved posts, and inspect posting status and analytics using the HumanPost MCP or Publishing API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milesfeldstein](https://clawhub.ai/user/milesfeldstein)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators and teams use this skill to connect to HumanPost, prepare and preview media posts, publish only with authorization, and review account, queue, task, and analytics status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized posts can become public, and queued status alone does not confirm publication.

Mitigation: Confirm the target account, content, and schedule before publishing; verify the final outcome with post or task status.

Risk: Uploads, previews, and tasks send content to HumanPost and may consume credits.

Mitigation: Review the destination and content, and create previews or tasks only within the user's request.

Risk: A company API key can expose account access if disclosed or granted excessive permissions.

Mitigation: Keep the key in a secret store or environment variable, use only the needed company-scoped permissions, and never print or share it.

## Reference(s):

- [HumanPost MCP setup](https://humanpost.com/docs/mcp)
- [HumanPost API documentation](https://humanpost.com/llms.txt)
- [HumanPost API fallback](references/api.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Analysis, Configuration instructions, Shell commands]

**Output Format:** [API requests, content drafts, and concise status or analytics reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posting and other consequential changes require user authorization; queued work is not confirmation of publication.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
