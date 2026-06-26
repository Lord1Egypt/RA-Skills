## Description: <br>
美团外卖红包 helps users claim Meituan coupons and red packets, authenticate a Meituan account, and query coupon claim history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to claim Meituan coupons or red packets, complete Meituan account verification, view coupon status and validity, and optionally set a daily automatic coupon-claiming reminder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests Meituan account verification data and stores account tokens and a persistent device identifier locally. <br>
Mitigation: Install only if the publisher is independently trusted, keep the runtime private, avoid exposing tokens or verification codes, and clear stored credentials when access is no longer needed. <br>
Risk: The skill can create a daily automatic coupon-claiming job that performs account actions without a fresh prompt each day. <br>
Mitigation: Review cron settings before enabling automation, keep the scheduled time intentional, and disable the job when automatic claiming is no longer wanted. <br>
Risk: Coupon history is stored locally by token and masked phone, and shared credential/cache tooling may retain more state than expected. <br>
Mitigation: Review local cache locations, remove stored histories and credentials during offboarding or account changes, and avoid sharing the same workspace across users. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/meituan-openplatform/meituan-waimai-coupon) <br>
- [Authentication Flow](references/auth-flow.md) <br>
- [Scheduled Coupon Claim Rules](references/cron-rules.md) <br>
- [Response Copy Templates](references/response-copy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with inline shell commands and JSON script outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store local Meituan tokens, a persistent device identifier, coupon claim history, and optional daily coupon-claiming schedule preferences.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
