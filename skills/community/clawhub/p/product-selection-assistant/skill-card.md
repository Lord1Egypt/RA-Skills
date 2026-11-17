## Description:

Helps ecommerce operators evaluate a product or ASIN by researching market signals, scoring demand, competition, profit, seasonality, entry difficulty, and growth trend, then producing a recommendation and interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators use this skill to assess whether a product is worth listing, especially for cross-border Amazon US marketplace decisions. It gathers public market information, creates six weighted scores, summarizes risks and opportunities, and produces prioritized launch actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute untrusted product or web-search text as browser code.

Mitigation: Escape HTML and JavaScript-sensitive report fields, use safe serialization for generated data, and treat produced reports as untrusted HTML until reviewed.

Risk: Reports may include public web-search information that is incomplete, stale, or misleading for commercial listing decisions.

Mitigation: Use the report as decision support only, verify key market and cost assumptions independently, and review high-impact recommendations before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/product-selection-assistant)
- [Publisher profile](https://clawhub.ai/user/bettermen)
- [Chart.js runtime dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summary plus generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The HTML report includes a six-dimension score model, Chart.js radar chart, analysis cards, and prioritized action items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
