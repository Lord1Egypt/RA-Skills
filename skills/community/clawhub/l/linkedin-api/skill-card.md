## Description:

Connects an agent to LinkedIn through Maton to retrieve profile and organization information, share posts, and manage advertising with user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting LinkedIn account holders can retrieve profile, organization, and advertising information, and prepare approved posts, media uploads, or campaign changes. Scheduled actions can be configured through Maton after the user confirms the account and intended automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A new connection or excessive OAuth scopes could expose the wrong account or more LinkedIn data than needed.

Mitigation: Confirm the intended account and scopes before connecting; use least privilege and revoke unused connections.

Risk: Posts, media uploads, campaign changes, or ad budgets could have public or financial consequences.

Mitigation: Show the exact account, content, media file, targeting, budget, and destination URL; obtain explicit approval before each write.

Risk: Persistent triggers could repeat actions after the initial request.

Mitigation: Confirm the function, schedule or event, and destination before enabling automation; review or disable it when no longer needed.

## Reference(s):

- [LinkedIn skill release](https://clawhub.ai/byungkyu/skills/linkedin-api)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [LinkedIn API overview](https://learn.microsoft.com/en-us/linkedin/)
- [LinkedIn Marketing API](https://learn.microsoft.com/en-us/linkedin/marketing/)
- [Time trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command, code, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [LinkedIn API responses depend on the authorized account and granted OAuth scopes.]

## Skill Version(s):

1.2.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
