## Description:

Make phone calls through the macOS Phone/FaceTime app and let an OpenClaw agent speak into the call via local TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flexrox](https://clawhub.ai/user/flexrox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to place explicitly authorized outbound calls from a Mac through the local Phone/FaceTime stack and speak generated text through local TTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real outbound calls through the local macOS Phone/FaceTime stack.

Mitigation: Require explicit user permission and verify the exact E.164 phone number before each live call.

Risk: macOS Accessibility/Automation control can interact with broad system dialogs while placing calls.

Mitigation: Grant permissions only to the intended runner, avoid running the skill while unrelated dialogs are open, and prefer --no-confirm or another explicit approval workflow.

Risk: Generated speech may be played into an active call through local TTS.

Mitigation: Review or constrain agent-generated text before speaking it into calls, especially in customer-facing or regulated contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flexrox/skills/phone-call)
- [Apple Phone User Guide for Mac](https://support.apple.com/guide/phoneapp/make-or-receive-calls-phn28c9d643a/mac)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for macOS calling and local TTS workflows; it does not produce inbound telephony services.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
