## Description:

Turn hotel amenity stills the property already took into one hotel amenity video per labeled still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel property and marketing teams use the skill to turn each named, approved amenity still into a short individual facility clip, then review and deliver the generated videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared authorization includes music, speech, and voice-management access that this workflow does not need.

Mitigation: Review the requested permissions before connecting and request narrower access; avoid proceeding until unnecessary scopes are addressed.

Risk: Selected photos leave the user's computer, paid generation spends Beatra credits, and installation analytics are automatic.

Mitigation: Use only stills authorized for upload, confirm paid generation before submitting, and account for automatic analytics in installation decisions.

Risk: Removing the package may disconnect other Beatra skills when installation records are malformed.

Mitigation: Review and correct the uninstall inventory before removal, and verify which connected skills may be affected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/hotel-amenity-clip)
- [Beatra skill page](https://beatra.ai/skills/hotel-amenity-clip)
- [Workflow guide](artifact/references/workflow.md)
- [Installation and authorization guide](artifact/references/installation-and-auth.md)
- [Updates and security guide](artifact/references/updates-and-security.md)
- [Uninstall and disconnect guide](artifact/references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Video artifacts, Text guidance, API Calls]

**Output Format:** [Labeled amenity-clip plan, generated video files, and task or billing results]

**Output Parameters:** [One clip per still; 2–15 seconds per clip]

**Other Properties Related to Output:** [Uses named property-provided stills; generated clips are reviewed before delivery.]

## Skill Version(s):

0.2.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
