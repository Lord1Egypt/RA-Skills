## Description:

Turns a product photo and merchant supplied details into a short vertical product video with spoken narration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and ecommerce teams use this skill to turn a real product photo and verified product details into a short vertical video with narration for product listings and social storefronts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad account access and a persistent shared credential.

Mitigation: Review the requested account access and decide whether a shared persistent credential is acceptable before authorizing the skill.

Risk: The security evidence flags automatic installation and environment reporting.

Mitigation: Review the installation registration disclosures and reported environment details before use.

Risk: The security evidence raises concern that product images or narration may be sent to Beatra without clear disclosure; the scan is partial.

Mitigation: Avoid uploading sensitive media until its handling is understood, and review the available security and release materials before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/product-video-studio)
- [Beatra Product Video Studio page](https://beatra.ai/skills/product-video-studio)
- [Writing the narration](artifact/references/copy-craft.md)
- [Commerce video workflow](artifact/references/workflow.md)
- [Installation registration](artifact/references/installation-registration.md)
- [Updates and security](artifact/references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Video, Image, Audio, Text, Subtitles]

**Output Format:** [A vertical product video with narration, an opening frame, a short script, and aligned subtitles in JSON, SRT, or VTT when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One clip, up to 15 seconds; the default script target is about 12 seconds.]

## Skill Version(s):

0.2.9 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
