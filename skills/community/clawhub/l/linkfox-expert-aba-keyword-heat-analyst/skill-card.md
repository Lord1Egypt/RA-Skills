## Description:

专注亚马逊ABA搜索词周维度热度分析，批量拉取多词多周SFR走势对比升温/掉热，支持Top ASIN点击转化份额、同比季节性对比、长尾词回退、关键词扩展与HTML可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon marketplace operators and ecommerce analysts use this skill to compare weekly ABA Search Frequency Rank trends for keyword lists, brands, product images, or ASIN-derived search terms. It supports trend tables, year-over-year seasonality checks, Top ASIN share context, keyword expansion, CSV links, and HTML dashboard reports while routing out-of-scope requests such as absolute search volume, sales, BSR, price, or launch date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and account workflows require LinkFox API keys and may include onboarding, billing, or payment-related actions.

Mitigation: Install only when LinkFox is trusted, avoid overriding gateway environment variables, and require explicit human review before any API-key, account, billing, or payment action.

Risk: File upload behavior can publish local artifacts through publicly accessible URLs.

Mitigation: Upload only files intended for public sharing and review file content, type, and size before requesting a public URL.

Risk: Generated HTML reports can carry unsafe or misleading content when built from untrusted keywords, URLs, or model output.

Mitigation: Review and sanitize report inputs and generated HTML before opening, sharing, or hosting the report.

Risk: Self-modification behavior can change or extend the skill beyond the reviewed release behavior.

Mitigation: Treat skill changes as a new review event and scan modified artifacts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aba-keyword-heat-analyst)
- [Primary skill definition](artifact/SKILL.md)
- [ABA keyword heat API reference](artifact/skills/amazon-aba-kw-heat/references/api.md)
- [ABA keyword heat contract](artifact/skills/amazon-aba-kw-heat/references/contract.json)
- [ABA keyword heat report layout](artifact/skills/amazon-aba-kw-heat-report/references/layout.json)
- [Amazon suggestion miner API reference](artifact/skills/linkfox-amazon-suggestion-miner/references/api.md)
- [Amazon widget miner API reference](artifact/skills/linkfox-amazon-widget-miner/references/api.md)
- [File upload API reference](artifact/skills/linkfox-file-upload/references/api.md)
- [AI text generation API reference](artifact/skills/linkfox-aigc-textgen/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown tables and summaries, JSON or CSV links when requested, and generated HTML report file paths for dashboard workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state that lower SFR values are hotter, identify keyword sources for image or ASIN workflows, and mark unavailable ABA data without inventing absolute search volume.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
