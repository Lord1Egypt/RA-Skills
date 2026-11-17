## Description:

Generate music and audio via Kie.ai's Suno gateway for background tracks, instrumental beds, full songs with vocals, or extending existing audio clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benhuebner01](https://clawhub.ai/user/benhuebner01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate or extend music and audio through Kie.ai's Suno gateway, including background tracks, instrumental loops, vocal songs, and audio variations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill reads more local OpenClaw environment secrets than it needs for music generation.

Mitigation: Install only if this behavior is acceptable; isolate KIE_API_KEY from unrelated secrets in OpenClaw globalEnv or ask the publisher to narrow loading to KIE_API_KEY and KIE_WEBHOOK_HMAC_KEY.

Risk: The skill can use Kie.ai credits and write generated audio and cover files under the selected output directory.

Mitigation: Confirm credit use before invoking the skill and choose an output directory intended for generated media files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benhuebner01/skills/kie-audio)
- [Kie.ai API key setup](https://kie.ai/api-key)
- [Kie.ai API endpoint](https://api.kie.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, API Calls]

**Output Format:** [JSON stdout plus downloaded audio and cover image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KIE_API_KEY; may download multiple generated tracks and cover images per request.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
