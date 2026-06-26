## Description: <br>
Provides internal-control leaders with a risk dashboard that combines complaints, logistics anomalies, and supplier scoring into daily reports, weekly forecasts, heatmaps, alerts, and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal-control and risk-management teams use this skill to turn operational inputs into concise risk summaries, prioritized action lists, daily and weekly reports, and management-facing trend views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references glossary, SOP, and rule-update documents that are not included in the artifact. <br>
Mitigation: Verify the referenced documents or define equivalent local procedures before relying on thresholds, escalation rules, or conflict handling. <br>
Risk: Risk reports may include sensitive complaints, logistics, supplier, or financial-loss data. <br>
Mitigation: Provide only data the user is authorized to analyze and keep generated reports within approved internal audiences. <br>
Risk: Automated report delivery, escalations, supplier actions, or external sharing could trigger business decisions without review. <br>
Mitigation: Require explicit human approval before automating pushes, escalations, supplier actions, or any external sharing. <br>
Risk: Pattern thresholds and trend signals can be inaccurate if not calibrated to the operating environment. <br>
Mitigation: Calibrate thresholds with real operating data, review false positives and false negatives, and revisit threshold performance periodically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/inter-control-07-risk-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style reports, tables, heatmaps, trend summaries, and action lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for internal risk-management review and depend on authorized, complete input data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; artifact frontmatter describes risk-dashboard instructions as v1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
