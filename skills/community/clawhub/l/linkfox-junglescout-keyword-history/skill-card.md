## Description:

Jungle Scout关键词历史搜索量查询，按7天周期返回亚马逊关键词的精确搜索量趋势，覆盖美国、英国、德国、日本等10个站点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce analysts use this skill to query Jungle Scout historical exact-match keyword search volume and evaluate seasonal demand, trend direction, and peak or low periods across supported Amazon marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can consume paid LinkFox/Jungle Scout credits.

Mitigation: Confirm user intent before repeated, expanded, or exploratory queries, and disclose that the skill documentation lists a 64-credit cost.

Risk: Account onboarding and billing flows can handle phone-code login, API keys, package selection, and payment orders.

Mitigation: Run onboarding or payment commands only after explicit user request, and avoid storing API keys in shell profiles on shared machines.

Risk: Automatic feedback reporting can send interaction details to LinkFox without a separate confirmation.

Mitigation: Do not include sensitive user or business details in feedback content, and disclose feedback submission when it is relevant to the user.

Risk: Keyword query results and cache files are persisted locally under a linkfox data directory.

Mitigation: Use the saved files only for the current task, and review or remove local data on shared workspaces when queries may reveal sensitive product research.

## Reference(s):

- [Jungle Scout keyword history API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-junglescout-keyword-history)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON API responses with optional Markdown tables, trend summaries, shell commands, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The query result is saved under a local linkfox session data directory; large responses are summarized unless full inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
