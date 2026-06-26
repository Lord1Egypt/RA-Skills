## Description: <br>
Reads Meta Ads campaigns, ad sets, ads, and creatives to support diagnostics, reports, and operational recommendations through the brijr/meta-mcp MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moskoweb](https://clawhub.ai/user/moskoweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, operators, and agent users use this skill to analyze Meta Ads performance, locate funnel bottlenecks, separate facts from hypotheses, and prepare daily, weekly, executive, tactical, or post-test reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and export Meta Ads performance data, including spend, campaign structure, creative details, and performance metrics. <br>
Mitigation: Install it only where brijr/meta-mcp is trusted, scope access to the intended Meta Ads accounts, and review exported insights before sharing. <br>
Risk: Recommendations may be misleading when Meta Ads data diverges from landing page, CRM, or financial data. <br>
Mitigation: Treat tracking confidence as part of the diagnosis and clearly separate facts, hypotheses, and recommended next steps. <br>


## Reference(s): <br>
- [Metrics Glossary](references/metrics-glossary.md) <br>
- [Diagnostic Frameworks](references/diagnostic-frameworks.md) <br>
- [Report Templates](references/report-templates.md) <br>
- [Funnel Analysis](references/funnel-analysis.md) <br>
- [Anomaly Playbooks](references/anomaly-playbooks.md) <br>
- [Official Meta Measurement Notes](references/official-meta-measurement-notes.md) <br>
- [Meta Performance Marketing](https://www.facebook.com/business/ads/performance-marketing) <br>
- [Meta Advantage+ Placements](https://www.facebook.com/business/ads/meta-advantage-plus/placements) <br>
- [Meta Help: Learning Phase](https://www.facebook.com/help/447278887528796) <br>
- [ClawHub Skill Page](https://clawhub.ai/moskoweb/meta-ads-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text diagnostics and reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should distinguish facts, hypotheses, and recommendations, and should reduce confidence when tracking, CRM, or page data is suspect.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
