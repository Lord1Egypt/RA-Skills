## Description:

拼多多研究员 helps agents research Pinduoduo products, categories, keywords, competitors, stores, pricing, and user feedback, then generate an interactive HTML market analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, analysts, and agents use this skill to evaluate Pinduoduo opportunities and produce concise research reports for product, keyword, competitor, store, category, pricing, and user-insight workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute injected browser code from untrusted search-derived report data and load third-party chart code.

Mitigation: Review reports before opening or sharing them, escape all report fields, validate style and class values, protect inline JSON, and remove or secure the CDN dependency before deployment.

## Reference(s):

- [PDD Researcher homepage](https://github.com/bettermen/pdd-researcher)
- [拼多多平台知识库](references/pdd_platform_knowledge.md)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language summary plus an interactive HTML report generated from structured JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WebSearch/WebFetch evidence and a Python report generator; generated HTML should be reviewed before opening or sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
