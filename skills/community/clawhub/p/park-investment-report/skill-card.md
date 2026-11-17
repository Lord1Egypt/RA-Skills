## Description:

Generates HTML reports for industrial parks that summarize industry composition, leading sectors, peer benchmarks, supply-chain opportunities, and targeted investment-attraction lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Economic-development, investment-attraction, and strategy teams use this skill to generate Chinese HTML reports for industrial parks from a park name and optional focus industry, benchmark park, style, city, and data-cutoff inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include incorrect or sensitive business and investment-attraction recommendations.

Mitigation: Review recommendations and enterprise targeting data before sharing, especially when non-public strategy or enterprise information may be involved.

Risk: Generated HTML report files load Chart.js from a CDN when opened.

Mitigation: Confirm the runtime environment permits CDN loading, or adapt the report to use an approved local Chart.js asset before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/park-investment-report)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [HTML report with embedded CSS and Chart.js chart configuration, usually saved as a file in the session reports folder.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes structured analysis, charts, data-confidence notes, and prioritized investment-attraction recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
