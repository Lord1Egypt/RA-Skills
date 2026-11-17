## Description:

Turns a supplied public trading calendar and authorized still images into short talking clips that announce the calendar's session, holiday, and settlement details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Wealth advisors and educators use the skill to turn already-public trading-calendar facts into short narrated clips, one per authorized still image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account connection stores a persistent local token and grants broad account access.

Mitigation: Review the authorization before connecting, keep the credential private, and disconnect through the documented uninstall process when no longer needed.

Risk: Approved voice, speech, and video requests can consume credits.

Mitigation: Check live prices and obtain separate approval for each paid stage and its call count before submitting.

Risk: The bundled client automatically replaces package files by default.

Mitigation: Review updates before installation or disable automatic updates with the documented update command.

Risk: Installation and coarse runtime details are sent to Beatra during registration.

Mitigation: Review the registration data and account privacy terms before connecting.

Risk: Cloned voices and animated likenesses may be used without proper rights.

Mitigation: Confirm likeness and voice permissions explicitly before uploading samples or generating media.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/market-calendar-talking)
- [Calendar talking workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Audio, Video clips]

**Output Format:** [Markdown slot plan and generation results with audio and video artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normally 2–8 separate clips, each 2–15 seconds; no stitched video.]

## Skill Version(s):

0.1.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
