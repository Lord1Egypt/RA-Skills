## Description:

Shopify Partner (shopify.com). Use this skill for ANY Shopify Partner request — reading, creating, and updating data. Whenever a task involves Shopify Partner, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Shopify Partner users use this skill to read organization, app, event, and transaction data, and to run Shopify Partner GraphQL queries or mutations through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions direct the agent to run a remote installer that was not included in the reviewed package.

Mitigation: Prefer a verified CLI release; otherwise inspect the installer and explicitly approve its local changes before execution.

Risk: The hosted connector accesses the user's Shopify Partner account, and GraphQL mutations can change account state.

Mitigation: Use only appropriate account permissions and retain confirmation for mutations.

## Reference(s):

- [Shopify Partner](https://www.shopify.com/partners)
- [Shopify Partner API documentation](https://shopify.dev/docs/api/partner/latest)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON results, with explanatory text as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read account data or change Shopify Partner state; confirm the exact payload and effect before writes.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
