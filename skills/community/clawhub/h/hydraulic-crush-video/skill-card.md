## Description:

Generates vertical hydraulic-press crushing short videos from text prompts or public object images using WeryAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to turn short text briefs or public HTTPS object images into vertical hydraulic-press crushing videos, with prompt expansion, parameter checks, WeryAI task submission, polling, and playable video URL reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed generation calls can consume paid WeryAI credits.

Mitigation: Review the expanded prompt and parameters before confirmation, use dry runs where appropriate, and avoid repeated wait runs unless new paid tasks are intended.

Risk: The skill requires WERYAI_API_KEY and sends prompts or public image URLs to WeryAI.

Mitigation: Use the skill only with a trusted publisher and WeryAI account, keep the API key out of source files, and avoid submitting sensitive prompts or private image URLs.

Risk: Image-to-video inputs must be publicly reachable HTTPS URLs.

Mitigation: Use only intended public image assets and verify the URL before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/hydraulic-crush-video)
- [WeryAI video generation API host](https://api.weryai.com)
- [WeryAI video models registry host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads; final responses include generated video URLs or clear error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access to WeryAI, user confirmation before paid generation, and public HTTPS image URLs for image-to-video.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
