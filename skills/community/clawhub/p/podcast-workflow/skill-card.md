## Description:

Podcast Workflow turns a transcript or audio URL into show notes, chapter markers, social media clips, SEO metadata, and a newsletter summary in one structured response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ash2hsa](https://clawhub.ai/user/ash2hsa)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, podcasters, and content teams use this skill to convert episode transcripts or public episode URLs into publish-ready podcast marketing assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch arbitrary user-provided podcast, video, RSS, or transcript URLs with curl.

Mitigation: Use only public URLs intended for agent access; avoid private links, internal services, authenticated pages, local file URLs, and confidential transcripts unless URL-fetching protections are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ash2hsa/skills/podcast-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Structured Markdown with timestamp lists, social post text, SEO fields, and newsletter copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use curl to fetch public podcast, video, RSS, or transcript pages when the user provides a URL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
