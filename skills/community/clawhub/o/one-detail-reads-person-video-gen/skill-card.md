## Description:

Create vertical short-form videos that frame a respectful social cue as a thesis, example beat, playful debate closer, and timed English captions using WeryAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content operators use this skill to turn a single social cue into a short vertical psychology-style video with timed English subtitles. It supports text-to-video, image-to-video, and limited multi-image video generation through WeryAI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can upload arbitrary readable local files to WeryAI when given a non-HTTPS image path.

Mitigation: Use public HTTPS image URLs by default; only use local paths after review and explicit consent, and avoid paths containing secrets, credentials, private documents, or workspace configuration.

Risk: The skill requires a WERYAI_API_KEY for paid network API calls.

Mitigation: Run in a limited workspace with an isolated or short-lived WERYAI_API_KEY and avoid exposing the key in prompts, logs, or generated files.

Risk: Social-cue prompts can drift into targeting, harassment, or professional diagnosis.

Mitigation: Keep examples generic and filmable, avoid real or private individuals and protected groups, and do not present outputs as professional psychology advice.

## Reference(s):

- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/one-detail-reads-person-video-gen)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown video link or concise status/error text, with optional shell command examples for WeryAI generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and paid WeryAI API usage.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
