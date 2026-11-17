## Description:

LinkFoxAgent helps agents run cross-border e-commerce research workflows for product discovery, marketplace analysis, keyword and review insights, patent research, sourcing, trend tracking, image and PDF analysis, and report generation across Amazon, TikTok, eBay, Walmart, Shopee, Ozon, 1688, and related data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to delegate cross-border e-commerce market research, product selection, competitor analysis, sourcing checks, patent research, image/PDF analysis, and report-generation tasks to LinkFoxAgent-backed tools. It is most relevant when the user has a LinkFoxAgent API key and, for ERP workflows, appropriate Lingxing OpenAPI credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, outputs, and generated artifacts may be sent to external services and surfaced through public links.

Mitigation: Do not use secrets, unreleased product plans, confidential ERP exports, sensitive personal data, or private images unless public sharing and external processing are acceptable.

Risk: Lingxing ERP workflows can access broad business data and may support write-capable operations.

Mitigation: Use least-privilege Lingxing credentials, prefer read-only access where possible, and avoid write-capable ERP applications unless the workflow explicitly requires them.

Risk: Local task outputs, token state, or cached artifacts may retain sensitive business context after execution.

Mitigation: Clear local output and token caches after sensitive work and review generated file paths before sharing results.

## Reference(s):

- [LinkFoxAgent homepage](https://agent.linkfox.com/)
- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/skills/linkfoxagent)
- [Amazon frontend reference](references/amazon-frontend.md)
- [Amazon data insight reference](references/amazon-data-insight.md)
- [Keepa reference](references/keepa.md)
- [SellerSprite reference](references/seller-sprite.md)
- [Lingxing ERP reference](references/lingxing-erp.md)
- [Patent research reference](references/patent.md)
- [Sandbox and PDF reference](references/sandbox.md)
- [AI tools reference](references/ai-tools.md)
- [Web search reference](references/web-search.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with links, local file paths, inline shell commands, and generated artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs may return a public ShareURL and may generate downloadable CSV, Excel, image, HTML, or attachment artifacts.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
