## Description:

AI-powered meeting optimization tool that analyzes calendar events, provides efficiency scores, extracts action items, and automates follow-ups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacealllc](https://clawhub.ai/user/jacealllc)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external professionals, and developers use this skill to analyze meetings, produce efficiency scores, extract action items from notes, and generate briefing or report output for meeting follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store API keys and task-manager tokens in local configuration and can print the full configuration.

Mitigation: Do not use real secrets until secure secret storage and output redaction are added; review configuration output before sharing logs.

Risk: The notes processor can read meeting notes from arbitrary local file paths supplied by the user.

Mitigation: Process only files from explicitly trusted paths and avoid using the command on sensitive or untrusted note files.

Risk: Setup runs mutable dependency installation with npm install.

Mitigation: Review package dependencies and install in an isolated environment before using the skill with real data.

Risk: The artifact advertises calendar and task integrations that are partly mock or incomplete.

Mitigation: Validate integration behavior with non-sensitive sample data before relying on calendar, task, or automation results.

## Reference(s):

- [Meeting Efficiency Pro API Documentation](references/api-docs.md)
- [ClawHub skill listing](https://clawhub.ai/jacealllc/skills/meeting-efficiency-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with inline command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces meeting briefings, note summaries, action items, efficiency scores, recommendations, and weekly reports.]

## Skill Version(s):

1.0.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
