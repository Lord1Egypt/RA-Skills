## Description:

Moyu performs daily maintenance for an OpenClaw-style workspace, including status checks, self-review, memory organization, and task recording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayadododo](https://clawhub.ai/user/ayadododo)

### License/Terms of Use:

MIT-0

## Use Case:

Agents or operators use this skill to run routine workspace maintenance: checking identity, memory and daily logs, comparing available skills with tool definitions, and producing a concise status report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect private user notes, memories, logs, and capability information during routine maintenance.

Mitigation: Review the skill before installation and define explicit file allowlists and redaction rules for sensitive workspace content.

Risk: Scheduled runs can repeatedly summarize sensitive workspace information without a fresh approval step.

Mitigation: Enable recurring execution only after adding confirmation controls or after confirming the workspace does not contain sensitive notes, memories, logs, or task history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayadododo/skills/lobster-keeper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status report with operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workspace maintenance summaries derived from identity, memory, log, and skill-availability files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
