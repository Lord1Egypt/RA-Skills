## Description:

Nex Decision Journal helps agents log decisions, predictions, follow-up reviews, searchable history, exports, and judgment statistics in a local decision journal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to record important business or personal decisions, capture reasoning and confidence, review outcomes, and analyze decision-making patterns over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Export paths are not contained, so export commands could write outside the expected export location.

Mitigation: Review export commands before execution and use only simple filenames without slashes, backslashes, or parent-directory segments.

Risk: The journal can contain sensitive business or personal reasoning in local SQLite and exported files.

Mitigation: Avoid recording secrets, credentials, or regulated data, and restrict access to the journal directory and exported files.

Risk: Broad triggers could cause an agent to inspect or summarize sensitive decision history unexpectedly.

Mitigation: Run list, search, stats, reflect, and export commands only when the user clearly requests decision-journal access or confirms the action.

## Reference(s):

- [Nex Decision Journal on ClawHub](https://clawhub.ai/nexaiguy/skills/nex-decision-journal)
- [Nex AI Homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and plain-text CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local SQLite journal data and CSV or JSON exports under the user's configured decision journal directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
