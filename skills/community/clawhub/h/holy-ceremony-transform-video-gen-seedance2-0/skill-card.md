## Description:

Transforms a text brief or public HTTPS image into a holy ceremony and celebration styled Seedance 2.0 video request through WeryAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to turn short event briefs or public image URLs into confirmed WeryAI Seedance 2.0 video-generation requests with gold-white ceremonial lighting, confetti, dignified motion, and optional ambience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled CLI can submit broader paid video-generation requests than the advertised Seedance-only workflow.

Mitigation: Review the confirmation table before execution and keep requests scoped to model SEEDANCE_2_0 with the documented duration, aspect ratio, resolution, and audio options.

Risk: The skill requires a WERYAI_API_KEY and paid API calls.

Mitigation: Use an isolated or short-lived environment, avoid committing the key, and confirm each generation request before running wait commands that may consume credits.

Risk: Prompts and image inputs are sent to WeryAI, and image inputs must be public HTTPS URLs.

Mitigation: Avoid sensitive prompts and non-public image URLs; use only content appropriate for submission to the external video-generation service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/holy-ceremony-transform-video-gen-seedance2-0)
- [ClawHub publisher profile](https://clawhub.ai/user/zoucdr)
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JSON]

**Output Format:** [Markdown confirmation tables and inline video links, with JSON CLI responses from WeryAI generation commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces playable video URLs when generation completes; requires Node.js 18+, WERYAI_API_KEY, network access, and paid WeryAI requests.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
