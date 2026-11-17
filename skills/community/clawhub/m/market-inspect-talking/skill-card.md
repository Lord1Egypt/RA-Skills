## Description:

Turns office-supplied merchant inspection notices and authorized still images into short spoken market-inspection clips, one per image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Market-supervision staff use the skill to turn their own merchant notices and authorized portraits or notice graphics into a labeled set of short talking clips. It plans the clips before requesting approval for paid speech and video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra authorization has broad access across installed Beatra skills.

Mitigation: Review the requested authorization scope before approving, keep the credential private, and disconnect through the documented uninstall procedure when no Beatra skills remain.

Risk: Installed code can update silently by default.

Mitigation: Disable automatic updates with the documented update command if changes must be reviewed before installation.

Risk: Selected notices, stills, and generated media are sent to Beatra; installation metadata is registered.

Mitigation: Confirm the notices, media rights, and registration disclosures are acceptable before using the service.

Risk: Speech and video generation consume paid credits, and the final charge can differ from an estimate.

Mitigation: Review the live price and approve each paid stage before submission; check the reported final charge.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/market-inspect-talking)
- [Beatra skill homepage](https://beatra.ai/skills/market-inspect-talking)
- [Merchant notice talking workflow](artifact/references/workflow.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Video files]

**Output Format:** [Labeled Markdown plan followed by separate short talking clips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually 2–8 clips, one per still; each clip is 2–15 seconds, with delivered media details and actual credit charges when available.]

## Skill Version(s):

0.1.9 (source: ClawHub release and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
