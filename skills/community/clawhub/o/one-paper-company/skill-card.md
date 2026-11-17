## Description:

Generates a shareable, offline, printable single-page HTML research report for one company, with a 10-step scrollytelling flow, 15 data visualizations, inline ECharts, and pixel-style brand animation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research teams use this skill to turn company and quarter inputs into a self-contained HTML research page with market, financial, industry, and monitoring-signal visualizations. The current implemented form is the heavy cycle-review report; quick cards, valuation maps, and competitive landscape outputs are described as roadmap items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports built from untrusted web or JSON data may include active HTML or JavaScript content.

Mitigation: Open and share generated reports only when the source data is trusted; add sanitization and CSP hardening before accepting arbitrary inputs.

Risk: The skill can perform web searches, fetch company pages, run local Python scripts, and write HTML files to a user-selected path.

Mitigation: Review the planned data sources and output path before execution, and inspect generated HTML before distributing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardwason/skills/one-paper-company)
- [Project Homepage](https://github.com/EdwardWason/one-paper-company)
- [ECharts](https://echarts.apache.org/)
- [Product Forms](references/product-forms.md)
- [Data Contract](references/data-contract.md)
- [Responsive Specification](references/responsive-spec.md)
- [Exception Handling](references/exception-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated self-contained HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local output.html file at a user-specified path; generated reports inline JavaScript, ECharts, pixel-font assets, and supplied research data for offline viewing.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
