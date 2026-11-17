## Description:

SellerSprite (sellersprite.com). Use this skill for ANY SellerSprite request — reading, creating, and updating data. Whenever a task involves SellerSprite, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace sellers and product researchers use this skill to retrieve SellerSprite product, competitor, keyword, and API usage data and to research products. The research_products action is marked as a write in the skill and requires confirmation of its exact payload before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup directs the agent to run downloaded CLI software, while the installer and server-side connector have not been verified.

Mitigation: Review and approve CLI installation separately using a verified release, check automatic skill synchronization settings, and retain the skill's confirmation requirement for data changes. OOMOL handles SellerSprite credentials server-side.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [SellerSprite](https://www.sellersprite.com/)
- [SellerSprite API documentation](https://open.sellersprite.com/api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis, Guidance]

**Output Format:** [JSON data and concise text summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent inspects each action schema before sending input; state-changing product research requires confirmation of the exact payload.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
