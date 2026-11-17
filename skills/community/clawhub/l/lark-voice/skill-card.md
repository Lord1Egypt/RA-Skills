## Description:

Send voice messages on Lark (Feishu) by converting text to speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheerwhy](https://clawhub.ai/user/cheerwhy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn requested text into speech and send it as a Lark or Feishu voice message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared temporary audio paths under /tmp/openclaw/ can expose local file-safety issues on multi-user or shared systems.

Mitigation: Use a unique private temporary directory for each run and clean up generated audio files after the voice message is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheerwhy/skills/lark-voice)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an Opus audio file for delivery through the Lark message tool.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
