## Description:

Build a fit-scored subreddit pool, match content to the best communities with posting angles, and rewrite posts natively for Reddit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsandtea](https://clawhub.ai/user/bitsandtea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to research Reddit communities for a brand, select suitable posting angles for existing content, and prepare Reddit-native drafts for human review and posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand and content material is sent to an authenticated PostKing MCP service.

Mitigation: Install only when use of the connected PostKing account and service is acceptable for the user's brand and content data.

Risk: Suggested Reddit drafts or posting angles could conflict with subreddit rules or promotion norms.

Mitigation: Review the skill's rule_to_watch and promotion_mode guidance before manually posting on Reddit.

Risk: The skill prepares Reddit content but does not publish posts automatically.

Mitigation: Keep a human review and posting step in the workflow.

## Reference(s):

- [PostKing MCP endpoint](https://mcp.postking.app/mcp)
- [PostKing: Reddit Growth on ClawHub](https://clawhub.ai/bitsandtea/skills/postking-reddit)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown and structured tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces subreddit research, ranked recommendations, posting angles, rule and promotion-mode guidance, and review-ready Reddit draft copy.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
