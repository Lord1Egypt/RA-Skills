## Description:

Helps users arrange Meituan local errands, including pickup and delivery, shopping, queueing, and other rider assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenfang055-gif](https://clawhub.ai/user/shenfang055-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Users arrange same-city Meituan errands with pickup and delivery addresses, contact details, and an order preview before confirming a paid request.

### Deployment Geography for Use:

Mainland China (supported cities only)

## Known Risks and Mitigations:

Risk: Bundled obfuscated code and an under-disclosed background updater warrant review before installation.

Mitigation: Install only if the publisher is trusted; review the global pt-passport installation and cliguard updater first.

Risk: Account access, saved addresses, and phone details expose sensitive user information.

Mitigation: Use only your own authorized account and verify address and contact details before proceeding.

Risk: Submitting an order initiates a real, payment-related transaction.

Mitigation: Review the actual fee preview and confirm each order explicitly before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/shenfang055-gif/skills/meituan-paotui)
- [Server-resolved source repository](https://github.com/shenfang055-gif/meituan-paotui)
- [Commands and parameters](references/commands.md)
- [Order and address parameters](references/params.md)
- [Error handling](references/errors.md)
- [Meituan developer credentials](https://developer.meituan.com/zh/v2/dev/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown order previews, confirmation prompts, and order status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masks phone numbers in chat and presents actual preview fees before order submission.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
