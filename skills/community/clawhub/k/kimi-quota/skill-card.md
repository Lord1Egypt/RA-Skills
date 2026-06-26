## Description: <br>
查询 Kimi API 用量、订阅额度和账户信息。当用户询问"Kimi 额度"、"API 用量"、"剩余次数"、"订阅状态"或需要查看 Kimi Code 使用情况时使用。支持加密保存登录态，首次配置后自动查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MuseLinn](https://clawhub.ai/user/MuseLinn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Kimi users use this skill to query Kimi Code/API quota, subscription status, rate-limit windows, and remaining feature allowances from a local command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Kimi login cookie and can save it locally, so the cookie should be treated as account access. <br>
Mitigation: Use only the requested Kimi cookie, run the skill only on a trusted machine, avoid saving the cookie on shared or managed systems, and run the documented --clear command when the saved login state is no longer needed. <br>
Risk: If the cryptography dependency is missing, the script warns that the cookie will be stored in plaintext. <br>
Mitigation: Install cryptography before using --save, or provide a session token without saving it. <br>


## Reference(s): <br>
- [Kimi](https://www.kimi.com) <br>
- [Kimi subscription page](https://www.kimi.com/membership/subscription) <br>
- [ClawHub skill page](https://clawhub.ai/MuseLinn/kimi-quota) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/MuseLinn) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text quota report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save, load, or clear a local Kimi login cookie; saved cookies are encrypted when cryptography is installed.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
