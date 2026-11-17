## Description:

Chase's three-stage investment analysis system helps structure stock and AI-sector research using survival rules, A-X framework analysis, bull/bear debate, industry-chain mapping, and decision criteria for A/H/US markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chase-zhouchang](https://clawhub.ai/user/chase-zhouchang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to organize investment research, compare bull and bear cases, map AI industry-chain opportunities, and draft structured stock-analysis reports. Outputs should be treated as informational research rather than personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce concrete trading suggestions, including buy, sell, hold, target-price, stop-loss, and position-size guidance.

Mitigation: Treat outputs as informational research only, require explicit invocation, and verify current market data and suitability with qualified financial review before acting.

Risk: The skill uses broad triggers that may activate during ordinary financial discussions.

Mitigation: Limit activation to intentional investment-research requests and ask for confirmation before generating trading recommendations.

Risk: The artifact asks the agent to save final output to memory without defining a scoped storage location.

Mitigation: Disable or override memory-saving unless a user-approved storage path and retention policy are set.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chase-zhouchang/skills/investment-framework-bundle)
- [Skill Definition](artifact/SKILL.md)
- [V1 Original Framework](artifact/v1-original.md)
- [V2 Original Framework](artifact/v2-original.md)
- [V3 Original Framework](artifact/v3-original.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown stock-research reports with tables, scores, debate summaries, decision rules, and buy/sell/hold guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first investment research workflow; no fixed token limit or machine-readable output contract is specified.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
