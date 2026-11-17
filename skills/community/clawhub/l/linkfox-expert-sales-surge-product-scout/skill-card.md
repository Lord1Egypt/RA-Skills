## Description:

Amazon sales-surge product scouting skill for finding products that meet monthly sales and month-over-month growth thresholds, switching sort orders, running repeat checks, scheduling tasks, and delivering Excel-only results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators and ecommerce analysts use this skill to scout Amazon products with established sales and rising demand, preview the top candidates, export complete Excel results, and optionally apply preference-based ASIN scoring. It supports LinkFox-powered product search, file delivery, and recurring scouting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send LinkFox API credentials to endpoints controlled through environment configuration.

Mitigation: Treat LINKFOX_AGENT_API_KEY as a secret and keep LINKFOX_TOOL_GATEWAY unset or pinned to the official HTTPS gateway before use.

Risk: A bundled scoring patch helper can persistently rewrite agent instruction files.

Mitigation: Do not run patch_scoring_to_agent.py or its --all mode unless persistent instruction changes are intentional and reviewed.

Risk: Uploaded deliverables can become publicly accessible URLs.

Mitigation: Upload only files that are approved for public sharing and review generated Excel or report content before upload.

Risk: Scheduled scouting can repeatedly consume LinkFox credits.

Mitigation: Confirm schedule frequency, parameters, and expected credit cost before enabling recurring tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-sales-surge-product-scout)
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai)
- [SellerSprite Product Search API Reference](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [Product Scout API Parameter Catalog](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [Dynamic Scoring Expectations Example](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [File Upload API Reference](artifact/skills/linkfox-file-upload/references/api.md)
- [Task Scheduler API Reference](artifact/skills/linkfox-task-scheduler/references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown conversation output with inline shell commands, JSON status snippets, and Excel file deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary deliverables are Excel workbooks for scouting and scoring results; uploads may produce public HTTPS URLs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
