## Description:

Launch Retro Analyzer helps agents run D1/W1/M1 launch retrospectives by comparing channel actuals to targets, analyzing the largest miss with 5-Whys, making keep/kill/change decisions, drafting learnings, and preparing a launch-registry outcome snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, and launch teams use this skill after a launch to turn targets, analytics exports, and platform dashboard numbers into a structured retrospective with channel decisions and next-launch learnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analytics exports, dashboard screenshots, or pasted launch data may include sensitive or untrusted content.

Mitigation: Only provide analytics exports suitable for this workflow, treat external data as untrusted input, and label every figure as Measured, User-provided, or Estimated.

Risk: Retrospective summaries and outcome snapshots may persist launch analytics or decisions.

Mitigation: Require user confirmation before saving results and review proposed saved content before confirming persistence.

Risk: Platform self-reported metrics can be mistaken for the authoritative launch result.

Mitigation: Keep platform-reported numbers in a reference column and use UTM-attributed own analytics as the truth column.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/launch-retro-analyzer)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown retrospective with tables, a 5-Whys narrative, keep/kill/change decisions, learnings, and a reviewed persistence proposal]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Every figure is labeled Measured, User-provided, or Estimated; UTM-attributed own analytics are treated as the truth column and platform-reported numbers as reference.]

## Skill Version(s):

19.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
