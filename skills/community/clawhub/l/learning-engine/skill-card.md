## Description:

Auto-analyze mistake and success patterns and reflect in skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to review errors, self-evaluations, and performance data, then convert recurring patterns into learned rules, reports, and skill updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learned rules or automatic edits may introduce incorrect or misleading guidance into other skills.

Mitigation: Run in dry-run or review-first mode where possible and require human approval before changing skill instructions.

Risk: Learning data writes can spread sensitive or unreviewed content into long-lived rules.

Mitigation: Limit write access to a dedicated learning-data area and review generated rules before reuse.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown and JSON files with concise guidance and skill instruction updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist learned rules, weekly reports, event records, and proposed edits to skill instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
