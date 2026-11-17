## Description:

Provides internal control leaders with an end-to-end risk dashboard that combines complaint, logistics exception, and supplier score signals into daily reports, weekly forecasts, heat maps, alerts, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal control owners and risk operations teams use this skill to turn complaint, logistics, supplier, and priority incident data into management-facing daily reports, weekly outlooks, heat maps, and immediate highest-risk summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for internal risk reporting and may handle complaint, logistics, and supplier-risk information.

Mitigation: Install only in internal workspaces where the intended control owners may view those datasets.

Risk: Scheduled or push delivery of reports could expose sensitive operational risk data to unintended recipients.

Mitigation: Configure explicit recipients for automated delivery and review outputs before external sharing.

Risk: Risk thresholds and trend judgments may be inaccurate if the underlying inputs are incomplete or not calibrated to real operations.

Mitigation: Require the report to identify data gaps, calibrate thresholds with operational history, and review high-priority actions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/inter-control-07-risk-dashboard)
- [Publisher profile](https://clawhub.ai/user/nic-yuan)
- [Unified glossary](docs/GLOSSARY.md)
- [Insufficiency handling](docs/INSUFFICIENCY-HANDLING.md)
- [Rule update SOP](docs/RULE-UPDATE-SOP.md)
- [Output conflict adjudication](docs/LINKING-SOP.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, tables, heat maps, alerts, and concise risk summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include priority-ranked action lists, trend interpretations, and notes about data gaps when inputs are incomplete.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
