## Description:

Connects an agent to IssueBadge to issue, verify, revoke, and export digital certificates and badges, manage dynamic QR codes, and integrate via MCP or API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[issuebadge2026](https://clawhub.ai/user/issuebadge2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other IssueBadge users can connect an agent to manage digital credentials, retrieve certificate data, and configure integrations after authorizing access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized actions may issue or revoke real public credentials, including sending recipient emails that cannot be recalled.

Mitigation: Confirm the template, recipient, and revocation details before changes; use idempotency keys when issuing credentials.

Risk: Exposing API keys or access tokens could allow unauthorized access to IssueBadge.

Mitigation: Prefer OAuth when available; never request secrets in chat or echo them in responses.

## Reference(s):

- [IssueBadge skill release](https://clawhub.ai/issuebadge2026/skills/issuebadge)
- [IssueBadge MCP integration guide](https://issuebadge.com/h/integration/mcp)
- [IssueBadge developer documentation](https://issuebadge.com/h/developer)
- [IssueBadge MCP server source](https://github.com/issuebadge/mcp-server)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, API calls, Shell commands]

**Output Format:** [Text or Markdown with configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide public credential verification links and retrieved certificate data.]

## Skill Version(s):

1.0.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
