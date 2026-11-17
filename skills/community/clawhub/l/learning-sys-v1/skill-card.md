## Description:

Helps OpenClaw users turn AI research, coding work, and weekly study activity into structured learning notes, recaps, knowledge maps, and mastery reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI practitioners use this skill to organize learning plans, create deep-dive notes, recap implementation work, update an AI knowledge map, and generate weekly learning reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw memory logs and learning notes while producing summaries, health reports, and mastery scores.

Mitigation: Use it only in an intended OpenClaw workspace and review the notes and memory files that will be summarized.

Risk: Weekly review behavior may send summaries through Feishu without clear confirmation.

Mitigation: Disable sending or explicitly confirm the recipient and message contents before running weekly review workflows.

Risk: The --quick option can skip confirmation checkpoints.

Mitigation: Avoid --quick until the files, planned changes, and communication steps have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/learning-sys-v1)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Deep Dive Template](artifact/references/deep-dive-template.md)
- [Knowledge Map Rules](artifact/references/knowledge-map-rules.md)
- [Quality Checklist](artifact/references/quality-checklist.md)
- [Recap Template](artifact/references/recap-template.md)
- [Weekly Review Guide](artifact/references/weekly-review-guide.md)
- [Weekly Review Template](artifact/references/weekly-review-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, checklists, reports, shell commands, and optional JSON mastery-score output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local OpenClaw notes and memory logs when producing health reports, weekly reviews, and mastery scores.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.yaml; artifact _meta.json lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
