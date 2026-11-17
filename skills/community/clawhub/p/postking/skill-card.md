## Description:

First-run flow for PostKing: authenticate, top up credits, onboard a brand from a URL, connect socials, and ship a first post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsandtea](https://clawhub.ai/user/bitsandtea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to take a new PostKing setup from authentication through credits, brand onboarding, social account connection, and the first scheduled post. It is also used to recover from authorization, credit, or trial-blocking states before returning to day-to-day content work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing steps can initiate a top-up or subscription.

Mitigation: Before any top-up or subscription, confirm the exact price, tier or pack, and billing path in the current conversation.

Risk: Social connection and post approval steps can affect public marketing channels.

Mitigation: Confirm the platform, account connection intent, post content, and schedule before generating OAuth links or approving a post.

## Reference(s):

- [PostKing skill listing](https://clawhub.ai/bitsandtea/skills/postking)
- [PostKing MCP endpoint](https://mcp.postking.app/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with tool names and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before billing, OAuth/social connection, onboarding, and post approval steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
