## Description: <br>
Embedded UX research skill that passively observes interactions, administers post-task and end-of-day surveys, captures verbatim quotes, detects friction and delight signals, and generates daily insight reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giulianomorse](https://clawhub.ai/user/giulianomorse) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and product teams use this skill to collect local UX research observations, post-task survey responses, end-of-day reflections, and daily insight reports about OpenClaw usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts broad passive observation by default and records users' exact words in persistent local files. <br>
Mitigation: Enable it only for intended UX research sessions, confirm how to pause observation, and reduce or redact verbatim capture where possible. <br>
Risk: Observation and survey logs may include sensitive conversation content if used during private work. <br>
Mitigation: Avoid use during sessions involving credentials, customer data, private code, health, legal, financial, or other sensitive material, and delete ~/.uxr-observer when data should be removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/giulianomorse/observer) <br>
- [Clawsight Analysis Framework](references/analysis-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Local JSONL observations and surveys, Markdown daily reports, and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data locally under ~/.uxr-observer and can generate per-day reports from local records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
