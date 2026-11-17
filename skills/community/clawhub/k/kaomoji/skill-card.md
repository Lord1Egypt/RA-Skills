## Description:

Light kaomoji selector based on context tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxuanyuan](https://clawhub.ai/user/wxuanyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to pick a context-appropriate kaomoji, list the bundled kaomoji set, or add tagged kaomojis for later use in conversational output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The save command can update the bundled kaomoji list, so shared or agent-writable installations may accumulate unreviewed text that later appears in conversations.

Mitigation: Review added entries when multiple users or agents can modify the skill folder, and install only where local JSON updates are acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text, JSON, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local tag matching against the bundled kaomojis.json data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
