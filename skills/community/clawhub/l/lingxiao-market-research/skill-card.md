## Description:

Helps agents run Lingxiao cross-border e-commerce market research by checking category-country demand, competition, price bands, and keyword intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeli20221102-ux](https://clawhub.ai/user/mikeli20221102-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and e-commerce analysts use this skill to evaluate whether a category-country market is worth entering, classify keyword demand by purchase intent, and form evidence-backed next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-research queries, category and country parameters, and network metadata may be sent to Lingxiao's MCP service.

Mitigation: Avoid submitting confidential product plans, customer data, credentials, or internal strategy unless the user trusts Lingxiao's service and privacy terms; use MCP approval prompts where available.

Risk: Unavailable category-country combinations can return errors that may be mistaken for evidence that a market has no demand.

Mitigation: Check available options before requesting a report and treat unsupported combinations as data unavailability, not as a market conclusion.

Risk: Search volume, competition scores, intent classification, and partial coverage can be misread as definitive sales evidence.

Mitigation: Cross-check findings with price bands, reviews, ad search-term reports, and response coverage indicators before making commercial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeli20221102-ux/skills/lingxiao-market-research)
- [Lingxiao MCP endpoint](https://www.lingxiaochuhai.com/mcp)
- [Lingxiao market research](https://www.lingxiaochuhai.com/market-research)
- [Lingxiao service pricing](https://www.lingxiaochuhai.com/service-pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown prose with JSON configuration snippets and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include category-country market summaries, keyword intent groupings, evidence-backed recommendations, and caveats about coverage or quota limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
