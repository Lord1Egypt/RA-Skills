## Description: <br>
Helps users claim Meituan coupons, check current promotions, search nearby in-store dining group-buy products, and create Meituan orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fhao233](https://clawhub.ai/user/fhao233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Meituan users use this skill to claim coupons, discover local dining deals, confirm location-specific offers, and place in-store dining group-buy orders through guided prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Meituan login state, local credential storage, and precise recent-location workflows. <br>
Mitigation: Install only when the publisher is trusted with this data, avoid granting persistent recent-location access unless needed, and use logout or device-token clearing when access should end. <br>
Risk: Scheduled coupon claiming and bundled CLIGuard self-update or daemon behavior can create persistent background activity. <br>
Mitigation: Review the scheduled auto-claim and CLIGuard behavior before use, enable scheduling only intentionally, and disable reminders when background activity is not desired. <br>
Risk: The skill can create Meituan in-store dining group-buy orders after user confirmation. <br>
Mitigation: Confirm product, merchant, price, quantity, location, and payment details before proceeding with order creation or payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fhao233/meituan-huisheng-coupon) <br>
- [Diagnostic guide](references/DOCTOR.md) <br>
- [Skill service terms](references/terms-of-service.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and concise user-facing text, with JSON-producing shell commands used internally by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include coupon tables, login or payment QR-code image links, order links, and status messages.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
