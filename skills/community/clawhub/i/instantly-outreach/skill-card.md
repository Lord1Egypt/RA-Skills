## Description:

Manage cold email campaigns, leads, and outreach analytics via Instantly AI through the superagnt unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use AI agents to manage Instantly campaigns, leads, sending accounts, and outreach analytics through Superagnt. The skill also supports related account settings and lead workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an account-credit lookup that does not match the stated outreach purpose, and the skill sends requests to Superagnt using an API key.

Mitigation: Review the credit lookup and confirm you are comfortable using Superagnt and providing it your API key before installing.

Risk: The documented API can send messages, delete or update records, change settings, and access billing or API-key administration.

Mitigation: Use only endpoints needed for the user's request, confirm before destructive or outbound actions, and require explicit authorization for account administration, key creation, billing changes, or purchases.

## Reference(s):

- [Superagnt Instantly integration documentation](https://superagnt.com/r/ch-instantly-outreach-docs)
- [Superagnt MCP client setup](https://www.superagnt.com/install)
- [Connect an Instantly account](https://app.superagnt.com/dashboard/connections)
- [Superagnt API key setup](https://superagnt.com/r/ch-instantly-outreach-key)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with curl commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations may send emails, modify or delete records, change account settings, or manage billing and API keys, depending on the requested endpoint.]

## Skill Version(s):

2.0.14 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
