## Description: <br>
发票认证技能。税局登录、发票勾选认证、抵扣统计。适用于进项发票勾选、认证、统计等税务操作场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxt](https://clawhub.ai/user/zxt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Tax and finance operators use this skill to log in to electronic tax systems, check invoice certification status, submit or cancel invoice certification, and request or revoke deduction statistics. It supports workflows that require an API key for the skill.quandianfapiao.com service and tax-account credentials for some actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive tax credentials, API keys, and invoice certification actions. <br>
Mitigation: Avoid sharing apiKeys or passwords in chat or command-line history; prefer short-lived or manually supplied credentials and confirm invoice certification or statistics actions before execution. <br>
Risk: The skill can persist login details in a local .session file for automatic re-login. <br>
Mitigation: Remove the saved .session file after use, especially on shared machines or managed workstations. <br>
Risk: The skill depends on the third-party skill.quandianfapiao.com service for tax-invoice API operations. <br>
Mitigation: Review the service relationship, data handling expectations, and account authorization before using it with production tax data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zxt/invoice-cert) <br>
- [中兴通简税Skill平台](https://skill.quandianfapiao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call remote tax-invoice APIs and print JSON-formatted API responses or concise status summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
