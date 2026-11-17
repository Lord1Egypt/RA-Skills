## Description:

A voice and text ordering agent for pizza shops that handles custom pizza orders, delivery zone validation, upselling, Google Sheets menu and order logging, and ThumbGate checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

Pizza shop operators use this skill to guide an agent through taking voice or text orders, validating delivery eligibility, logging callback details, and reducing common customization mistakes before orders reach the kitchen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Displayed pricing is inconsistent across release metadata, skill frontmatter, and sales copy.

Mitigation: Verify the current price on the ClawHub listing before purchase, installation, or resale use.

Risk: Google Sheets menu and order logging can expose order data or credentials if over-permissioned.

Mitigation: Use narrowly scoped Google credentials and restrict sheets to only the menu and order log needed by the pizza shop.

Risk: Incorrect delivery zone or customization handling could lead to rejected orders, remakes, or customer follow-up.

Mitigation: Configure the delivery radius and ThumbGate checks before deployment, and require confirmation for callback numbers, half-and-half sauces, and mutually exclusive toppings.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/igorganapolsky/skills/pizza-ordering-agent)
- [Publisher profile](https://clawhub.ai/user/igorganapolsky)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown instructions with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires operator-supplied menu data, delivery radius, and Google Sheets configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
