## Description:

Analyzes a user-selected short-form video’s transcript and structure, then drafts an original script for the user’s topic using that structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketers use it to study a supplied Douyin, Xiaohongshu, or TikTok video and draft an original, shoot-ready spoken script around their own topic, with similar pacing and structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied share text is transmitted to LinkDigest, and the package cannot verify the service’s server-side deletion claims.

Mitigation: Submit only content you intend to share with LinkDigest and omit sensitive material.

Risk: Video retrieval can consume LinkDigest credits.

Mitigation: Use a dedicated LinkDigest key and set --max-credits to cap spending for a request.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-linkdigest-script-rewrite)
- [ClawHub skill release](https://clawhub.ai/jackchew7143/skills/linkdigest-script-rewrite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with title options, cover text, timed script sections, and a beat-to-script comparison table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided video link or share text, topic, and target duration. Full transcript and breakdown require LINKDIGEST_API_KEY; keyless access provides a limited summary.]

## Skill Version(s):

1.2.1 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
