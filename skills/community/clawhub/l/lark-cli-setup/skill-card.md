## Description: <br>
Guides an agent through installing lark-cli, completing Feishu/Lark user authorization, configuring token refresh, and validating access to Feishu services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingshang2024-cell](https://clawhub.ai/user/jingshang2024-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect a Feishu/Lark account to lark-cli, authorize broad user access, keep tokens refreshed, and verify document, calendar, messaging, mail, wiki, OKR, approval, and related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures broad Feishu/Lark account access and creates a scheduled background token-refresh job. <br>
Mitigation: Before running the refresh setup, confirm the target account or app, cron schedule, timezone, and the process for disabling or deleting the job. <br>
Risk: OAuth tokens and authorization state may remain active beyond the immediate setup session. <br>
Mitigation: Review authorization scope, token status, and refresh behavior after setup, and reauthorize or revoke access when the account or intended use changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jingshang2024-cell/lark-cli-setup) <br>
- [Publisher profile](https://clawhub.ai/user/jingshang2024-cell) <br>
- [Node.js](https://nodejs.org) <br>
- [npmmirror registry](https://registry.npmmirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OAuth device-flow steps, QR-code generation guidance, cron refresh configuration, and validation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
