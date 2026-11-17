## Description:

基于卖家精灵的亚马逊潜力单变体选品专家。适用于寻找变体结构简单、变体复杂度低、具备销量或增长信号、开发路径更清晰的单变体商品机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and e-commerce operators use this skill to find single-variation Amazon product opportunities with low variation complexity, recent listing dates, and sales growth signals. It supports continued scouting, alternate sorting, preference-based ASIN scoring, Excel exports, and scheduled scouting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled helper scripts can persistently modify other agents' instruction files when patching is run broadly.

Mitigation: Review helper scripts before installation and run patch_scoring_to_agent.py only when intentional, especially avoiding --all unless broad modification is desired.

Risk: The file upload helper can publish local files to publicly accessible URLs.

Mitigation: Upload only files that are safe to disclose publicly and confirm the intended audience before sharing generated URLs.

Risk: Credentials and requests are sent to endpoints configured through environment variables.

Mitigation: Keep LINKFOX_TOOL_GATEWAY and related endpoint variables pinned to trusted LinkFox hosts and protect LINKFOX_AGENT_API_KEY values.

Risk: Scheduled scouting tasks can consume credits and send notifications to configured destinations.

Mitigation: Confirm task frequency, expected cost, and webhook or notification recipients before creating or enabling schedules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-single-variation-potential-scout)
- [SellerSprite product API reference](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [Product scout API parameter catalog](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [Dynamic ASIN scoring expectations example](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [Task scheduler API reference](artifact/skills/linkfox-task-scheduler/references/api.md)
- [File upload API reference](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation output with preview tables, JSON status cues, shell commands, and Excel file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary file outputs are Excel workbooks such as scout_round{N}_new_products.xlsx and scoring_result.xlsx.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact profile states 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
