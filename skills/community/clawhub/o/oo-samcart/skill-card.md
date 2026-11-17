## Description:

SamCart (samcart.com). Use this skill for ANY SamCart request — searching and reading data. Whenever a task involves SamCart, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using SamCart can retrieve customers, orders, products, and subscriptions from their connected marketplace. They use the skill to search and read SamCart data through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute an unverified remote installer without a separate approval step.

Mitigation: Have a trusted administrator install a verified CLI version separately, and require approval before any additional installation.

Risk: Connecting SamCart gives OOMOL access to the selected account data.

Mitigation: Connect only the intended SamCart account and review the data access before enabling the skill.

## Reference(s):

- [SamCart API documentation](https://developer.samcart.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieved records depend on the user's connected SamCart marketplace and account permissions.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
