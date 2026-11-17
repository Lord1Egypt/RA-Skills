## Description:

Helps agents set, test, and change prices across value metrics, packaging, discounts, price increases, pricing research, pricing pages, compliance checks, and commercial deal structures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to produce pricing recommendations, price-change plans, discount policies, research plans, pricing-page guidance, and durable local pricing records for products, services, retail, marketplaces, and enterprise deals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically write, move, and delete local business and contact records.

Mitigation: Review or constrain writes to shared contacts, shared projects, legacy pricing folders, and any deletion or migration steps before deployment.

Risk: Pricing work can involve customer details, confidential competitor pricing, and other sensitive commercial information.

Mitigation: Require confirmation before storing customer details or NDA-covered competitor pricing, and keep credentials out of stored notes.

Risk: Durable price-book and pricing-history changes can influence future agent recommendations.

Mitigation: Require confirmation before changing durable price-book or history files, and review generated pricing artifacts before using them operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/pricing)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Clawic pricing skill homepage](https://clawic.com/skills/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and local note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce pricing recommendations, price books, policy drafts, research write-ups, project notes, and local memory updates for later agent use.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
