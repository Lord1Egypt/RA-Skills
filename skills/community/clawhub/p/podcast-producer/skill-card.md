## Description:

Turns a raw podcast transcript into show notes, social captions, episode titles, SEO tags, and chapter timestamps. Supports both AI-narrated and human-hosted podcast styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tetsuakira-vk](https://clawhub.ai/user/tetsuakira-vk)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast creators and content teams use this skill to turn episode transcripts into publish-ready promotional and metadata assets, including titles, show notes, chapter markers, social captions, and SEO tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript content may contain sensitive or private material.

Mitigation: Only provide transcript files and pasted text that the agent is allowed to read and process.

Risk: Generated show notes, captions, timestamps, and SEO tags may be incomplete or need editorial correction.

Mitigation: Review the generated package before publication, especially approximate chapter timings and platform-specific copy.

Risk: Installing from an untrusted command source can introduce supply-chain risk.

Mitigation: Use a trusted or pinned ClawHub installer command when the environment supports it.

## Reference(s):

- [Podcast Producer on ClawHub](https://clawhub.ai/tetsuakira-vk/skills/podcast-producer)
- [Publisher Profile](https://clawhub.ai/user/tetsuakira-vk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response with section headers, lists, timestamps, captions, and comma-separated tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five podcast publishing assets in one response and may ask for transcript, style mode, language, or short-transcript confirmation when needed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
