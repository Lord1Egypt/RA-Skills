## Description:

Format, prettify, minify, or validate JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and other users use this skill to format, minify, or validate JSON supplied in the current agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided JSON may contain secrets or sensitive data.

Mitigation: Avoid pasting secrets unless the user is comfortable having the agent process that text in the current session.

Risk: Invalid JSON may be mistaken for repaired JSON if the user expects automatic fixes.

Mitigation: Report parse errors clearly and suggest a repair-focused skill when the user asks to fix invalid JSON.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with JSON code blocks or validation messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preserve insertion order or sort object keys alphabetically when requested; reports parse errors for invalid JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
