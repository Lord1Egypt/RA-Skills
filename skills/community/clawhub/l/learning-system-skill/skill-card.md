## Description: <br>
Learning System helps an agent turn AI research, code work, and notes into structured knowledge maps, deep-dive notes, recaps, weekly reviews, health checks, and mastery scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echoVic](https://clawhub.ai/user/echoVic) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI practitioners use this skill in OpenClaw to organize learning activity, convert research and implementation work into durable notes, update an AI knowledge map, and produce learning health or mastery reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weekly review mode can aggregate local memory, notes, and code-change history and send a summary through Feishu without clear opt-in or preview controls. <br>
Mitigation: Require manual preview and redaction before sending weekly summaries, and confirm the Feishu recipient before enabling review mode, --quick, or cron automation. <br>
Risk: Learning records may include private work, customer data, credentials, unreleased research, or sensitive project details from memory logs and notes. <br>
Mitigation: Review generated notes and summaries before persistence or sharing, and avoid running automated review flows on workspaces that contain unredacted sensitive information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/echoVic/learning-system-skill) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Deep Dive Template](references/deep-dive-template.md) <br>
- [Knowledge Map Rules](references/knowledge-map-rules.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [Recap Template](references/recap-template.md) <br>
- [Weekly Review Guide](references/weekly-review-guide.md) <br>
- [Weekly Review Template](references/weekly-review-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text, with optional shell commands and JSON report output from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update persistent learning notes and reports in the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
