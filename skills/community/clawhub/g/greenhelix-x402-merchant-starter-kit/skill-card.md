## Description:

A guide for deploying an x402 paywalled crypto-native storefront with an Express.js app, SQLite product catalog, MCP server, human checkout rails, agent discovery endpoints, CI/CD deployment guidance, and nginx configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace operators use this guide to create and deploy a crypto-native digital storefront that can serve human buyers and AI agents through x402 payment flows, product catalogs, and MCP integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests sensitive environment variables for loading even though the release is a non-executable guide.

Mitigation: Do not provide GITHUB_TOKEN or DASHBOARD_SECRET merely to read the guide; create separate least-privilege deployment secrets only in the storefront environment.

Risk: Deployment examples involve private content delivery, payment handling, and admin access.

Mitigation: Keep the GitHub token restricted to one repository with read-only access, use a strong dashboard secret, and review the guide before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-x402-merchant-starter-kit)
- [Publisher profile](https://clawhub.ai/user/mirni)
- [x402 protocol](https://github.com/coinbase/x402)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix storefront reference](https://claw.greenhelix.net)
- [x402 facilitator endpoint](https://x402.org/facilitator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with inline code, shell command, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples require user-supplied deployment secrets and infrastructure.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
