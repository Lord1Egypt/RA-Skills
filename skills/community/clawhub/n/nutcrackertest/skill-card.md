## Description: <br>
Ethnographic UX research skill that passively observes OpenClaw usage, extracts interaction data, detects friction and delight signals, and generates structured daily research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giulianomorse](https://clawhub.ai/user/giulianomorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to analyze local agent session history, detect friction and delight patterns, and generate daily UX research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and stores sensitive OpenClaw conversation history. <br>
Mitigation: Run it only when local conversation analysis is intended, review generated data and reports before sharing them, and delete stored data when no longer needed. <br>
Risk: PII redaction is best-effort and may miss sensitive details. <br>
Mitigation: Inspect redacted outputs before display or distribution and avoid relying on the redactor as the only privacy control. <br>
Risk: Automated cron use can create ongoing local analysis and retained reports. <br>
Mitigation: Enable scheduled runs only after a manual review confirms the generated files and retention behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/giulianomorse/nutcrackertest) <br>
- [Publisher profile](https://clawhub.ai/user/giulianomorse) <br>
- [OpenClaw skill homepage](https://clawhub.com/skills/uxr-observer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON analysis data, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local python3 and jq; generated reports and analysis data are stored locally by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
