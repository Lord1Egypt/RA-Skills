## Description:

Creates vertical nation-resilience hook videos with timed English on-screen text, map flashes, resource-geography-defense beats, and a final risk twist using WeryAI video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn a country, region, or abstract nation-resilience brief into a short-form geopolitical video prompt, confirmation plan, WeryAI CLI command, and final video link or error.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted image parameters can cause local image files to be read and uploaded to WeryAI.

Mitigation: Use public HTTPS image URLs only, avoid local paths and file:// URLs, and require explicit consent before any local image upload path is used.

Risk: Video generation and local-image upload require WERYAI_API_KEY and can consume paid credits.

Mitigation: Use a limited or short-lived API key, keep key values out of files, and confirm the full prompt and request parameters before submitting generation jobs.

## Reference(s):

- [WeryAI video CLI and JSON](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/nation-resilience-hook-video-gen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with confirmation tables, JSON request snippets, shell commands, playable video links, and error summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; generation uses paid network calls and may return WeryAI task status before video links are available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
