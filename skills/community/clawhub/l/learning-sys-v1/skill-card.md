## Description: <br>
Provides an AI learning workflow for knowledge maps, deep-dive notes, implementation recaps, weekly reviews, mastery scoring, and learning-health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical learners use this skill to turn AI research, code changes, and project work into structured notes, knowledge-map updates, weekly reviews, and mastery reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weekly review may collect memory logs, notes, PRs, or code-change summaries that include private work. <br>
Mitigation: Review the data sources before running review mode, limit it to intended workspace paths, and remove sensitive content from notes before generating a weekly summary. <br>
Risk: The workflow includes a Feishu summary-sending step without clear destination or approval controls in the artifact. <br>
Mitigation: Remove or manually gate the Feishu sending step until the destination, payload, and approval process are explicit. <br>
Risk: The --quick mode and automated weekly cron use can skip confirmation before reading workspace activity or changing learning files. <br>
Mitigation: Avoid --quick and cron automation until the operator has confirmed the files read, files written, and any outbound sharing behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/learning-sys-v1) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Deep Dive Template](references/deep-dive-template.md) <br>
- [Knowledge Map Rules](references/knowledge-map-rules.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [Recap Template](references/recap-template.md) <br>
- [Weekly Review Guide](references/weekly-review-guide.md) <br>
- [Weekly Review Template](references/weekly-review-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated note, review, report, and JSON outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local OpenClaw workspace notes, memory logs, knowledge maps, deep-dive notes, and weekly review files.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
