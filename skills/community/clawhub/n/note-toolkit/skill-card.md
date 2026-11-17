## Description:

Knowledge capture and connection system that helps agents organize, classify, connect, and retrieve notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture note content, apply tags, organize knowledge, connect related notes, and retrieve stored information through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local command execution even though the release evidence does not show a clear need or concrete command limits.

Mitigation: Review the skill before installation; remove exec access or document specific allowed commands and confirmation requirements.

Risk: Note retrieval may require file search access, which can expose local note content or other files if scoped too broadly.

Mitigation: Limit file search to the intended note workspace and avoid storing sensitive information unless local access controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/note-toolkit)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return structured note data, summaries, classifications, retrieval results, troubleshooting guidance, and configuration steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
