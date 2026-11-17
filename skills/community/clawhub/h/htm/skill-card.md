## Description:

Helps HTM account holders review passes, products and trips, compare Regio Vrij subscriptions, and stage product orders for browser checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghuron](https://clawhub.ai/user/ghuron)

### License/Terms of Use:

MIT-0

## Use Case:

HTM account holders and authorized agents use this skill to review passes and trip history, assess subscription value, and add products to the HTM cart. The account holder completes any payment in a browser.

### Deployment Geography for Use:

The Netherlands

## Known Risks and Mitigations:

Risk: HTM account credentials and pass-owner birthdates may be exposed through logs or shared shells.

Mitigation: Use only accounts and passes you are authorized to manage; keep HTM_LOGIN, HTM_PASSWORD and birthdate variables out of logs and shared shells.

Risk: Ordering can stage items in an HTM shopping cart.

Mitigation: Review the cart in the browser before completing any payment.

## Reference(s):

- [Mijn HTM skill on ClawHub](https://clawhub.ai/ghuron/skills/htm)
- [HTM portal](https://www.htm.nl)
- [Skill command reference](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON from the CLI; natural-language guidance when used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Order commands can add or update a draft cart item; payment is not automated.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
