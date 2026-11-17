## Description:

Create vertical absence shorts with a quiet home, stalled phone, moving feed, bittersweet closer, and timed English captions using WeryAI, while avoiding self-harm content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and video-generation agents use this skill to produce short vertical absence videos with safe melancholic framing, explicit caption timing, and WeryAI-compatible generation parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, public HTTPS image URLs, and the WeryAI API key are sent to WeryAI for paid video generation.

Mitigation: Use the skill only when this data sharing is acceptable, keep WERYAI_API_KEY in the environment, and avoid private or sensitive image URLs.

Risk: The absence-video theme can overlap with vulnerable or self-harm-adjacent user requests.

Mitigation: Keep the framing to implied absence, refuse self-harm or suicide method content, and prefer hopeful last-line variants for vulnerable users.

Risk: Unsupported model parameters can cause WeryAI generation errors.

Mitigation: Use the documented model constraints, require a non-empty model, and omit unsupported fields such as negative_prompt for Seedance.

## Reference(s):

- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/if-you-vanished-video-gen)
- [WeryAI video tasks API host](https://api.weryai.com)
- [WeryAI models registry API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with WeryAI JSON parameters, inline shell commands, and a video URL or structured error]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and WeryAI paid video generation.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
