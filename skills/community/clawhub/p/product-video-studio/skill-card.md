## Description:

Create a short vertical product video with spoken narration from a product photo and merchant-supplied details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and ecommerce teams use the skill to turn one product photo and verified product details into a narrated vertical video for product listings, launches, and social posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports tracking and installation data collection.

Mitigation: Review the installation and telemetry disclosures before connecting, and proceed only if the reported data collection is acceptable.

Risk: Product content is transferred to external Beatra services for processing.

Mitigation: Upload only product photos and details you are authorized to share; keep sensitive content out of the workflow.

Risk: The security evidence reports broad access through a shared account authorization.

Mitigation: Review the requested account access and use an account with an appropriate scope before authorizing.

Risk: Uninstall or disconnect actions may affect credentials shared with other Beatra skills.

Mitigation: Read uninstall prompts and check whether other Beatra skills use the shared credentials before revoking or deleting them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/product-video-studio)
- [Beatra Product Video Studio page](https://beatra.ai/skills/product-video-studio)
- [First frame guidance](artifact/references/first-frame.md)
- [Narration and claims guidance](artifact/references/copy-craft.md)
- [Commerce video workflow](artifact/references/workflow.md)
- [Updates and security](artifact/references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Video, Audio, Image, Text, Subtitles]

**Output Format:** [A vertical video and supporting media, with a narration script and optional JSON, SRT, or VTT subtitles]

**Output Parameters:** [One clip, up to 15 seconds]

**Other Properties Related to Output:** [Optional product sound effects; the opening frame determines the video canvas.]

## Skill Version(s):

0.2.8 (source: server-resolved release; artifact/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
