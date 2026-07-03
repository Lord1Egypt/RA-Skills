## Description: <br>
MagicHaqi Operator is a developer- and owner-use agent that runs recurring MagicHaqi operations for marketing drafts, BYOC content production, demo pet care, and growth analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paraengine](https://clawhub.ai/user/paraengine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MagicHaqi owners use this skill to run a small recurring operations loop that creates owner-approved marketing assets, generates and verifies MagicHaqi content, maintains a demo pet, and writes daily KPI summaries from local state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL-token login can expose account access if copied into screenshots, logs, or shared links. <br>
Mitigation: Treat the URL token as a secret and avoid sharing screenshots or logs that include it. <br>
Risk: Autonomous recurring operation could produce unwanted marketing, content, or spending actions if left unsupervised. <br>
Mitigation: Install only in the MagicHaqi owner/developer environment, keep the documented cadence limits, and require explicit owner approval for spending or real third-party publishing. <br>
Risk: Persistent local state, journal, audit, marketing, and memory outputs may retain operational details longer than intended. <br>
Mitigation: Periodically inspect or clear the agent/ state, journal, audit, marketing, and memory outputs. <br>
Risk: Telemetry handling is unclear when sdk.remoteLog is accessible to analytics. <br>
Mitigation: Review what sdk.remoteLog exposes before enabling analytics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paraengine/haqi-operator) <br>
- [Haqi Operator playbook](artifact/PLAYBOOK.md) <br>
- [Haqi Operator schedule](artifact/schedule.md) <br>
- [Content production task](artifact/tasks/content.md) <br>
- [Marketing task](artifact/tasks/marketing.md) <br>
- [Analytics task](artifact/tasks/analytics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands, JSON state updates, generated content artifacts, KPI summaries, and shareable deep links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local agent/ state, journal, audit, marketing, and content outputs; third-party publishing and spending require explicit owner approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
