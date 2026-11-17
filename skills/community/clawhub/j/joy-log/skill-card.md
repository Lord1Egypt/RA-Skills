## Description:

Automatically records warm or joyful conversation moments and helps generate shareable joy cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericsma2019](https://clawhub.ai/user/ericsma2019)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to capture positive moments from conversations, preserve them as a joy log, and generate warm share cards from selected excerpts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic capture may save conversation excerpts that include sensitive or unintended personal content.

Mitigation: Disable auto_capture by default where possible, require explicit confirmation before each saved moment, and review or redact captured text before card generation.

Risk: Generated cards may be shared with a recipient before the user has reviewed the content.

Mitigation: Require user confirmation before sending or sharing any generated card, especially when sending to Eric or another named recipient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericsma2019/skills/joy-log)

## Skill Output:

**Output Type(s):** [Text, Files, Images, Configuration]

**Output Format:** [Markdown instructions, JSON moment records, and generated PNG card files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores captured moments under memory/joy-log and generated cards under memory/joy-log/cards when used as described.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
