## Description: <br>
Helps users authenticate to Meituan, claim Meituan Union coupons, view campaign links, manage coupon reminders, and troubleshoot coupon or authentication issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-union](https://clawhub.ai/user/meituan-union) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill in an agent to claim Meituan coupons, receive coupon reminders, manage local account state, and view related promotional activity links after consenting to the stated terms. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles phone/SMS login and stores local login and device identifiers. <br>
Mitigation: Install only from a trusted publisher, complete the consent flow before use, and review the logout and device-clearing commands before providing account information. <br>
Risk: Doctor diagnostics can expose raw tokens or log data. <br>
Mitigation: Run diagnostics only when explicitly needed and avoid sharing diagnostic output unless sensitive tokens and account data have been removed. <br>
Risk: The security review flags unsafe network settings and broad triggers. <br>
Mitigation: Prefer a version that narrows triggers and enables TLS certificate verification for all account-related requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-union/meituan-union-coupon-skill) <br>
- [Publisher profile](https://clawhub.ai/user/meituan-union) <br>
- [Doctor diagnostics guide](references/DOCTOR.md) <br>
- [Skill terms of service](references/terms-of-service.md) <br>
- [Meituan user service agreement](https://rules-center.meituan.com/rule-detail/4/1) <br>
- [Meituan privacy policy](https://rules-center.meituan.com/m/detail/guize/2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command snippets and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include coupon result tables, reminder prompts, account-management guidance, diagnostic summaries, and links to Meituan campaign or policy pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
