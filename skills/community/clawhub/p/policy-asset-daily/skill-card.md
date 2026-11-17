## Description:

Generates a bilingual Chinese/English single-file HTML daily report that links political policy, macro signals, energy, commodities, FX, and capital market movements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shrifill](https://clawhub.ai/user/shrifill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to produce a daily macro strategy report that connects current policy events and public market data to likely asset-class transmission paths. The report is intended for research reference and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated HTML report can contact TradingView when opened.

Mitigation: For offline or privacy-sensitive use, remove or disable the TradingView ticker widget before opening or sharing the report.

Risk: The report relies on public news and market sources that may be incomplete, delayed, or unsuitable as investment advice.

Mitigation: Verify important market data and source links independently, and treat the output as research material rather than a trading recommendation.

## Reference(s):

- [Policy-to-Asset Transmission Framework](artifact/references/linkage_framework.md)
- [Preferred News Sources by Domain](artifact/references/news_sources.md)
- [Base HTML Report Template](artifact/assets/report_template.html)
- [ClawHub Skill Page](https://clawhub.ai/shrifill/skills/policy-asset-daily)

## Skill Output:

**Output Type(s):** [text, code, files, guidance]

**Output Format:** [Single-file HTML report with inline CSS and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese/English report output; the TradingView ticker may load an external script when the generated HTML is opened.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
