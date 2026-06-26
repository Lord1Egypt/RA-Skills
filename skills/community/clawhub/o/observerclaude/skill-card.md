## Description: <br>
UxrObserver passively records OpenClaw usage, surveys users after tasks, and generates redacted UX research reports with charts under user-controlled sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giulianomorse](https://clawhub.ai/user/giulianomorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and product teams use this skill to capture local UX research observations, task outcomes, survey responses, and periodic reports about real usage patterns. It is suited for deliberate research logging where the user understands the retention and sharing posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill continuously records exact user activity and survey answers in local logs. <br>
Mitigation: Install it only for deliberate UX research, pause or delete the study when logging is not desired, and avoid confidential or credential-related work while it is active. <br>
Risk: Generated reports can be moved into Google Docs, Sheets, Drive, Gmail, or email. <br>
Mitigation: Review and redact reports before any sharing action, and require explicit user confirmation before sending or updating last-sent state. <br>
Risk: Research logs may retain personal, business, legal, medical, financial, or credential-related content if the user works on sensitive tasks. <br>
Mitigation: Use the documented redaction rules, inspect raw data on request, and apply the pause and delete controls regularly for retention management. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/giulianomorse/observerclaude) <br>
- [Publisher profile](https://clawhub.ai/user/giulianomorse) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Observation taxonomy](artifact/observation-taxonomy.md) <br>
- [Redaction rules](artifact/redaction-rules.md) <br>
- [Report template](artifact/report-template.md) <br>
- [Survey instruments](artifact/survey-instruments.md) <br>
- [Analysis framework](artifact/analysis-framework.md) <br>
- [Chart generator](artifact/generate-charts.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON and JSONL logs, chart image files, and user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local study data under ~/.uxr-observer/ and produces reports only for user-controlled sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
