## Description:

亚马逊低价商品选品专家，用于寻找或评估低价商品、价格带机会、平价细分市场、小额客单商品，并按低售价筛选候选商品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and product researchers use this skill to find low-price marketplace opportunities, compare sorting strategies, export spreadsheet results, and optionally run preference-based ASIN scoring. It supports supported Amazon marketplaces across US, UK, DE, FR, JP, CA, IT, ES, MX, and IN.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox API keys, product queries, generated files, and scheduled prompts may be sent to LinkFox services.

Mitigation: Install only in trusted LinkFox environments, keep API keys out of shell startup files where possible, and review product queries and generated files before use.

Risk: Credential routing is under-scoped and custom gateway or login endpoint environment variables can redirect requests.

Mitigation: Control the process environment and avoid custom gateway or login endpoint variables unless they are explicitly required and trusted.

Risk: A bundled patcher can persistently rewrite agent instruction files.

Mitigation: Do not run the CLAUDE.md patcher unless persistent agent-instruction changes are intentional and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-low-price-product-expert)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [Root skill instructions](artifact/SKILL.md)
- [SellerSprite product search API](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [Amazon product scout API parameter catalog](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [ASIN scoring example expectations](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [Task scheduler API](artifact/skills/linkfox-task-scheduler/references/api.md)
- [File upload API](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown conversation output with shell commands, JSON snippets, and generated Excel/JSON file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary product-selection and scoring deliverables are spreadsheet files; the skill also presents Top 10 previews and status or scheduling guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
