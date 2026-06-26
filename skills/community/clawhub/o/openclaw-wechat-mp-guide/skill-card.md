## Description: <br>
Guides an agent through connecting OpenClaw to a WeChat Official Account for automated message replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, media operators, and developers use this skill to configure WeChat Official Account credentials, OpenClaw connection settings, automated replies, keyword responses, transfer behavior, and message statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles WeChat API credentials and account connection secrets. <br>
Mitigation: Use a dedicated least-privilege WeChat account or test account, avoid printing credentials in checks, and keep environment files out of version control. <br>
Risk: Automated WeChat actions can affect a real public account. <br>
Mitigation: Require manual final approval before any draft, preview, publish, or account-facing action. <br>


## Reference(s): <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential placeholders and manual setup steps for WeChat and OpenClaw.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact files report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
