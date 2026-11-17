## Description:

跨文化电商选品专家，帮助跨境卖家、品牌方和选品团队基于目标国家或地区的文化、生活方式、节日气候、1688 采购关键词、Alexa 提示词和多源验证发现商品机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as cross-border sellers, brands, and product selection teams use this skill to generate culturally grounded product ideas for a target market, expand sourcing and validation keywords, and prioritize opportunities after Amazon, Google Trends, ABA, Alexa, and 1688-style validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security summary says the skill reports user feedback and sends API requests to LinkFox.

Mitigation: Install only when LinkFox API processing and possible feedback summaries are acceptable for the intended workspace.

Risk: The ClawHub security guidance notes that the skill handles LinkFox API credentials.

Mitigation: Use a scoped secret store for LINKFOX_AGENT_API_KEY or LINKFOXAGENT_API_KEY, avoid shell startup files, and avoid phone-code onboarding in shared terminals.

Risk: The ClawHub security guidance says uploaded files become publicly accessible URLs.

Mitigation: Review files before upload and avoid uploading confidential or regulated content through the file-upload workflow.

Risk: Endpoint environment variables can redirect requests away from expected LinkFox hosts.

Mitigation: Keep LINKFOX_* endpoint variables pinned to trusted HTTPS LinkFox hosts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-cross-cultural-product-scout)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [LinkFox Skills](https://skill.linkfox.com/)
- [Cross-cultural product selection workflow](artifact/skills/cross-cultural-product-selection/SKILL.md)
- [Amazon search competition schema](artifact/skills/linkfox-amazon-search-competition/schemas/serp-context-comparison.schema.json)
- [Report layout references](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and structured product-research guidance, with optional generated files and shell commands for LinkFox helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long product-selection outputs are routed to HTML report files; validation data should be presented with source traceability and without fabricated numeric claims.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
