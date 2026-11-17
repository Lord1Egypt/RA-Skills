## Description:

Manage and analyze Meta (Facebook/Instagram) Ads campaigns, including performance metrics, ad spend, ROAS, CPA, CTR, audience breakdowns, creative analysis, budget optimization, and approved campaign, ad set, or ad changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiddun](https://clawhub.ai/user/aiddun)

### License/Terms of Use:


## Use Case:

External advertisers, marketers, and agency operators use this skill to analyze Meta ad performance, audit campaigns, compare audiences and creatives, and prepare budget or campaign changes for user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved write actions can affect live Meta campaigns, budgets, ads, or paused and deleted objects.

Mitigation: Show the exact campaign, ad set, or ad field that will change, including current and proposed values, and require explicit user approval before any write.

Risk: The skill can inspect connected Meta ad accounts and performance data.

Mitigation: Install only when the agent should access those accounts, and return concise summaries limited to the data needed for the user's task.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown responses with tables, concise recommendations, and JSON-serializable tool outputs when calling Meta Ads tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should keep account data concise, aggregate metrics before returning them, cap ranked lists, format currency and percentages, and require explicit user approval before writes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
