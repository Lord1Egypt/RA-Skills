## Description:

Investment Analysis Workflow guides agents through an incremental investment research workflow for classifying new materials, reading archived reports first, updating ongoing analyses, maintaining stock pool evaluations, and producing structured research updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcchris1995](https://clawhub.ai/user/pcchris1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to keep investment research continuous when new announcements, research notes, industry news, or meeting notes arrive. The workflow emphasizes reading existing archived reports before producing incremental Markdown analysis, updating persistent investment files, and preserving traceability for changed profit assumptions or stock-pool judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can cause an agent to modify persistent local investment research files.

Mitigation: Require explicit user confirmation before edits or rewrites and keep backups or version control for the investment workspace.

Risk: The skill produces high-stakes investment analysis, including profit forecasts, PE judgments, and buy or sell ranges that may be incorrect or misleading.

Mitigation: Treat outputs as non-professional investment analysis, verify source data independently, and avoid using the skill as sole basis for trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pcchris1995/skills/investment-analysis-workflow)

## Skill Output:

**Output Type(s):** [guidance, markdown, files, analysis]

**Output Format:** [Markdown analysis updates and file-editing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append to or reorganize local investment research files when the hosting agent has file-editing capability.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
