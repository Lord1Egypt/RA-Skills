## Description: <br>
A Meituan coupon and ordering assistant that helps users find restaurants or group-buying deals, claim coupons, review product options, and place confirmed orders through the conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-union](https://clawhub.ai/user/meituan-union) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search nearby Meituan dining deals, claim coupons, compare product options, and place orders after explicit confirmation. The skill is intended for consumer dining and coupon workflows tied to a Meituan account and location context. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require Meituan account login and location access. <br>
Mitigation: Use only when the publisher is trusted, review the service rules before use, and confirm location sharing choices before enabling recent-location lookup. <br>
Risk: The skill can retain local authentication, location, and device state. <br>
Mitigation: Use account logout and device reset flows when access should be revoked, and avoid installing on shared or untrusted devices. <br>
Risk: Security evidence flags under-disclosed background updating, device fingerprinting, token/location persistence, broad automatic triggers, and a suspicious verdict. <br>
Mitigation: Review the skill carefully before installing and require explicit confirmation before any order or payment action. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/meituan-union/meituan-coupon-order-assistant) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/meituan-union) <br>
- [Skill service use rules](references/terms-of-service.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Conversational Markdown with product lists, confirmation prompts, links, and QR code images when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before order or payment actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
