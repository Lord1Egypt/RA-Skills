## Description:

Provides end-to-end NodeMaven proxy setup and usage guidance for proxy type selection, geo-targeting, access configuration, API key validation, and usage monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vkprosinnm](https://clawhub.ai/user/vkprosinnm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to choose, configure, and monitor NodeMaven residential or mobile proxies for account management, scraping, browser automation, and data collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to handle NodeMaven API keys, proxy credentials, and sub-user passwords in chat.

Mitigation: Use secure secret input or local environment variables, mask API keys, avoid repeating full proxy URLs, and do not persist credentials in saved artifacts.

Risk: The skill can guide persistent account-admin actions such as whitelist, sub-user, notification, mutation, or deletion operations.

Mitigation: Require explicit user confirmation before creating, updating, resetting, or deleting account resources.

Risk: Dashboard links include mandatory tracking parameters.

Mitigation: Disclose that tracked onboarding links are used when routing users to NodeMaven account, API key, or pricing pages.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/vkprosinnm/skills/nodemaven-premium-proxy)
- [Publisher Profile](https://clawhub.ai/user/vkprosinnm)
- [NodeMaven API Swagger Documentation](https://dashboard.nodemaven.com/documentation/v2/swagger/)
- [NodeMaven API Base](https://api.nodemaven.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, API request examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proxy setup steps, masked credential handling guidance, proxy URL templates, curl examples, and monitoring instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
