## Description: <br>
Manages Beisen iTalent overtime workflows by helping authorized users authenticate, submit overtime records, query scheduled overtime, and request overtime cancellation through the iTalent Open Platform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjm1226](https://clawhub.ai/user/zjm1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR staff, managers, and authorized employees use this skill to manage overtime records in Beisen iTalent, including authentication, overtime submission, overtime lookup, and cancellation requests. It should be used only by users who are authorized to manage the relevant employee overtime records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles AppKey, AppSecret, and access tokens for an HR system. <br>
Mitigation: Use least-privilege iTalent API credentials, avoid sharing secrets in chats or shell history, and use --save only when ~/.italent-overtime.conf is protected. <br>
Risk: The push and cancel commands can change live overtime records and initiate approval workflows. <br>
Mitigation: Require explicit human confirmation before push or cancel actions, including the target employee, overtime dates, reason, and overtime ID where applicable. <br>
Risk: A stale or overbroad token may allow unauthorized access to employee overtime data. <br>
Mitigation: Re-authenticate when tokens expire, rotate credentials as needed, and install the skill only for users authorized to manage the relevant iTalent records. <br>


## Reference(s): <br>
- [API interface documentation](references/api-docs.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Beisen iTalent Open Platform](https://open.italent.cn) <br>
- [iTalent token endpoint](https://openapi.italent.cn/token) <br>
- [ClawHub skill page](https://clawhub.ai/zjm1226/italent-overtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call live iTalent APIs and may write an access token to ~/.italent-overtime.conf when --save is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact files mention 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
