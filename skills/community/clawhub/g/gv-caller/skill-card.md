## Description:

Gv Caller uses Google Voice to place calls and play AI-generated speech or local audio to the recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe12801](https://clawhub.ai/user/joe12801)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw agent place Google Voice calls from natural-language requests or command-line arguments, then play text-to-speech output or a local audio file during the call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place Google Voice calls automatically from broad natural-language triggers.

Mitigation: Require explicit per-call confirmation and clear legal approval for each destination and message before execution.

Risk: The skill uses stored Google Voice session cookies that can grant account access.

Mitigation: Use protected cookie storage, a dedicated Google Voice account, and a contained, unprivileged runtime.

Risk: Temporary call audio may contain sensitive message content.

Mitigation: Use private temporary directories and remove generated audio after the call workflow completes.

## Reference(s):

- [Google Voice calls](https://voice.google.com/u/0/calls)
- [ClawHub skill page](https://clawhub.ai/joe12801/skills/gv-caller)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Audio, API Calls]

**Output Format:** [Markdown with inline shell commands and generated call audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary WAV audio and a call-result screenshot during execution.]

## Skill Version(s):

1.0.1 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
