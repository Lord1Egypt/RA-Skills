## Description:

Creates short spoken insurance renewal reminders from advisor-supplied dates and authorized still images, producing one talking clip per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance advisors and wealth educators use the skill to plan and generate short renewal-date reminder clips from their supplied schedules and authorized photos. Each still produces its own clip rather than a stitched video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Beatra device authorization permits credit spending, selected-media uploads, and access to Beatra tasks and artifacts beyond this clip workflow.

Mitigation: Grant access only if this broader account authority is acceptable; approve each paid generation stage, and review or revoke device access when finished.

Risk: Automatic package updates are enabled by default and can replace installed skill files without a separate approval.

Mitigation: Disable automatic updates for manual control and review updates before enabling them again.

Risk: Spoken renewal details or a person's likeness could be inaccurate or used without authorization.

Mitigation: Use only supplied schedule facts and authorized images or voice samples; review scripts and clips before sharing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/insurance-renew-talking)
- [Beatra skill homepage](https://beatra.ai/skills/insurance-renew-talking)
- [Renewal reminder talking workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Video clips, Audio files]

**Output Format:** [Markdown slot list and individual video artifacts, with optional synthesized audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 2–8 separate clips of 2–15 seconds each; no stitching. Reports available media details and charged credits.]

## Skill Version(s):

0.1.8 (source: server-resolved release and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
