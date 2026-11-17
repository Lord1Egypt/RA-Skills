## Description:

Manage an Instagram creator or business account through the InstantDM MCP tools by triaging and replying to comments, answering DMs, monitoring ad comments, pulling account and post insights, tracking follower trends, and working with the linked Facebook Page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanjaykhanssk](https://clawhub.ai/user/sanjaykhanssk)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and business account managers use this skill to review Instagram engagement, prepare approved replies, follow up in DMs, monitor Meta ad comments, and summarize performance trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved sends reach real Instagram or Meta users and consume InstantDM credits.

Mitigation: Review exact drafted replies, exact recipients, and total batch credit cost before approving any send action.

Risk: The InstantDM MCP URL contains an auth key that can expose account access if shared.

Mitigation: Treat the full URL containing auth=<key> like a password and avoid exposing it in logs, screenshots, or shared configuration.

Risk: Large batches or repeated identical messages can create account safety and rate-limit issues.

Mitigation: Keep batches small, vary message drafts, and stop immediately on credit-exhausted or rate-limit errors.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries, reply drafts, approval tables, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed public replies, private DM drafts, engagement classifications, performance summaries, and credit-aware batch plans.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
