## Description:

Provides six Chinese ACG-style persona voices for OpenClaw, enabling explicit role switching, multi-turn consistency, and clear technical-task responses with a light character frame.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjp-cn](https://clawhub.ai/user/wjp-cn)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to switch among six Chinese ACG-style persona voices for chat, support, and technical tasks while preserving clear task output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persona layer can make responses feel less suitable for professional or precision-heavy work.

Mitigation: Lower persona intensity for technical tasks or restore default behavior when the style interferes with clarity.

Risk: The selected voice can persist in local OpenClaw state.

Mitigation: Use the clear command or review local state behavior before deploying in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjp-cn/skills/moe-persona-theater)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and persona voice files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language persona guidance; selected voice may be persisted in local OpenClaw state]

## Skill Version(s):

1.0.0 (source: package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
