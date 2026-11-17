## Description:

Generates an interactive HTML daily gold and silver market report covering spot prices, China T+D and futures markets, macro indicators, gold-silver ratio analysis, institutional targets, and a bull/bear summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tusu168](https://clawhub.ai/user/tusu168)

### License/Terms of Use:

MIT

## Use Case:

External users and market-report builders use this skill to gather current gold and silver market data and render a structured Chinese-language daily HTML report. The report is intended for research and communication workflows, not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can embed untrusted HTML or JavaScript when report JSON contains untrusted text.

Mitigation: Review or harden the renderer before using untrusted JSON; prefer escaping plain text and generating structured HTML and JavaScript internally.

Risk: The HTML template loads ECharts from a remote CDN.

Mitigation: Vendor or integrity-pin ECharts before using the report in locked-down, offline, or authenticated environments.

Risk: Market data may contain conflicting timestamps, stale values, or noisy source readings.

Mitigation: Use the skill's cross-checking guidance, discard anomalous readings, and state the adopted data cutoff and market session in the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tusu168/skills/gold-silver-daily-report)
- [Data sources and methodology](references/data_sources.md)
- [Report template specification](references/template_spec.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Interactive HTML report generated from JSON market data, chart data, and template placeholders.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local file named 黄金白银日报-YYYY-MM-DD.html; report data should be gathered from current, cross-checked market sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
