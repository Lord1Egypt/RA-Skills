## Description:

Learning System helps an OpenClaw agent turn AI learning inputs, code work, research, and weekly reviews into structured knowledge maps, deep-dive notes, recaps, and progress reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echovic](https://clawhub.ai/user/echovic)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users use this skill to manage AI-domain learning by selecting deep-dive topics, writing study notes, recapping implementation work, updating a knowledge map, and running health or mastery-score reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weekly review behavior can summarize private memory logs, notes, PR activity, and work history, then send a Feishu summary without a clearly documented confirmation step.

Mitigation: Require a user preview and explicit recipient confirmation before sending any weekly summary, and disable scheduled review jobs unless that confirmation is enforced.

Risk: The skill's scripts read local OpenClaw workspace memory and notes, which may contain sensitive personal or work information.

Mitigation: Run the scripts only in the intended OpenClaw workspace, review the files they can access, and avoid sharing generated reports until their contents have been checked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/echovic/skills/learning-system-skill)
- [OpenClaw Agent](https://github.com/openclaw/openclaw)
- [Deep Dive Template](references/deep-dive-template.md)
- [Knowledge Map Rules](references/knowledge-map-rules.md)
- [Quality Checklist](references/quality-checklist.md)
- [Recap Template](references/recap-template.md)
- [Weekly Review Guide](references/weekly-review-guide.md)
- [Weekly Review Template](references/weekly-review-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, generated note templates, shell commands, tabular reports, and optional JSON from the mastery score script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The health and mastery scripts read local OpenClaw workspace notes and memory files, then print reports to standard output.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
