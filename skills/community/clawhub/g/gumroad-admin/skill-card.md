## Description:

Gumroad Admin CLI. Check sales, products, and manage discounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abakermi](https://clawhub.ai/user/abakermi)

### License/Terms of Use:


## Use Case:

Store operators and developers use this skill to administer a Gumroad store from an agent workflow, including checking sales, listing products, and creating discounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Gumroad access token that can expose or modify store data if mishandled.

Mitigation: Use the least-privileged Gumroad token available, keep it private, and provide it only through the required GUMROAD_ACCESS_TOKEN environment variable.

Risk: Discount creation commands can affect live product pricing.

Mitigation: Review discount creation commands, including product ID, code, amount, and discount type, before allowing them to run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abakermi/skills/gumroad-admin)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GUMROAD_ACCESS_TOKEN for Gumroad authentication.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
