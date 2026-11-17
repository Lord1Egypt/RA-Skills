## Description:

Reads Meta Ads campaigns, ad sets, ads, and creatives for diagnostics, reports, and operational recommendations using only the brijr/meta-mcp MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moskoweb](https://clawhub.ai/user/moskoweb)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, marketers, and analysts use this skill to inspect Meta Ads performance across account, campaign, ad set, ad, and creative levels, identify funnel bottlenecks, and produce concise diagnostics with next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured brijr/meta-mcp integration may access relevant Meta Ads account performance data.

Mitigation: Install only when that access is intended, review the MCP permissions, and limit account/data access to the needed analysis scope.

Risk: Performance recommendations can be misleading when tracking, CRM, landing page, or financial data is incomplete or inconsistent.

Mitigation: State confidence clearly, distinguish facts from hypotheses, and validate conclusions against Meta, page, CRM, and business outcome data before acting.

## Reference(s):

- [Meta MCP](https://github.com/brijr/meta-mcp)
- [Meta Ads Performance Marketing](https://www.facebook.com/business/ads/performance-marketing)
- [Meta Advantage+ Placements](https://www.facebook.com/business/ads/meta-advantage-plus/placements)
- [Meta Business Help](https://www.facebook.com/help/447278887528796)
- [Metrics Glossary](references/metrics-glossary.md)
- [Diagnostic Frameworks](references/diagnostic-frameworks.md)
- [Report Templates](references/report-templates.md)
- [Funnel Analysis](references/funnel-analysis.md)
- [Anomaly Playbooks](references/anomaly-playbooks.md)
- [Official Meta Measurement Notes](references/official-meta-measurement-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text diagnostics and reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates facts, hypotheses, and recommendations; reduces confidence when tracking, CRM, or landing page data is suspect.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
