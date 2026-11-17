## Description:

Generate a short video clip with sound on movoa.ai (MiniMax H3, Seedance 2.5, Veo 3.1 Fast, Seedance 2.0) with the user's own API key. Use when the user asks for a video from a text prompt or wants to animate a photo (photo to video), and MOVOA_API_KEY is set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanshs474](https://clawhub.ai/user/hanshs474)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request a short video with sound from a text prompt or ask to animate a photo. The skill checks the Movoa balance, presents the run details and credit cost for approval, then submits the generation after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and photo URLs may be sent to Movoa.

Mitigation: Avoid submitting sensitive prompts or photos; use only image URLs you are comfortable sharing with Movoa.

Risk: The security scan is incomplete because a local path-like reference could not be resolved.

Mitigation: Review the unresolved reference and rescan the complete skill package before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hanshs474/skills/movoa-video)
- [Movoa text-to-video](https://movoa.ai/video/text-to-video)
- [Movoa photo-to-video](https://movoa.ai/video/photo-to-video)
- [Movoa pricing](https://movoa.ai/pricing)
- [Movoa API key settings](https://movoa.ai/settings/apikeys)

## Skill Output:

**Output Type(s):** [Video, Text]

**Output Format:** [Generated video clip with sound and a video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Photo-to-video requires a public HTTPS image URL.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
