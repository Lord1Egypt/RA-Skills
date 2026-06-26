## Description: <br>
Monitors GitHub trending repositories by language and time range, then sends daily or on-demand notifications through Telegram, Discord, or email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhdryanchang](https://clawhub.ai/user/zhdryanchang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, open source contributors, and technical teams use this skill to track trending GitHub repositories, filter results by language and time range, and receive automated digests through configured notification channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an embedded SkillPay API key. <br>
Mitigation: Remove the key before use, rotate it with the provider, and require deployment-specific secret injection through environment variables or a secret manager. <br>
Risk: Subscription and payment controls are exposed without adequate access protection. <br>
Mitigation: Deploy only behind authentication or a private gateway, and authorize each subscription, notification, and payment operation for the requesting user. <br>
Risk: Payment callbacks may be accepted without signed provider verification. <br>
Mitigation: Require signed SkillPay callback verification before changing subscription state or logging paid usage. <br>
Risk: Notification and repository data may be sent to external services. <br>
Mitigation: Validate notification recipients, restrict CORS, and disclose data flows to Telegram, Discord, email, GitHub, and SkillPay before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhdryanchang/github-trending-monitor) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [GitHub Trending](https://github.com/trending) <br>
- [GitHub Repository Search API](https://api.github.com/search/repositories) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [REST API JSON responses, notification messages, and Markdown setup examples with shell commands and environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to GitHub, SkillPay, and any configured notification providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
