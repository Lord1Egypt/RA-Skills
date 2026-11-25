## Description:

Manage cold email campaigns, leads, and outreach analytics via Instantly AI through the superagnt unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams can use an agent to manage Instantly campaigns and leads, review outreach performance, and automate connected account workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup check requests account credits from the superagnt API, which also receives the supplied API key.

Mitigation: Use the integration only if you trust superagnt with the key, and confirm the credits check fits your intended use.

Risk: The connected account can send or forward email and make destructive or administrative changes, including deleting records or changing account settings.

Mitigation: Confirm outbound, destructive, billing, or credential-changing actions with the user, and call only the endpoints needed for the requested task.

## Reference(s):

- [Integration documentation](https://superagnt.com/r/ch-instantly-outreach-docs)
- [Connection setup](https://app.superagnt.com/dashboard/connections)
- [API key access](https://superagnt.com/r/ch-instantly-outreach-key)
- [ClawHub listing](https://clawhub.ai/superagnt/skills/instantly-outreach)

## Skill Output:

**Output Type(s):** [Shell commands, API requests, Guidance]

**Output Format:** [Markdown guidance with curl examples, endpoint tables, and request schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SUPERAGNT_API_KEY; actions use the connected Instantly account.]

## Skill Version(s):

2.0.19 (source: artifact frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
