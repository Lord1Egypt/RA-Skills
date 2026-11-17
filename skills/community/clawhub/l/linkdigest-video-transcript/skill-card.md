## Description:

Extracts spoken transcripts, on-screen text with approximate timestamps, key points, and engagement metrics from supported video links through LinkDigest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide supported public video links or share text to obtain a transcript, on-screen text with approximate timing, key points, and available engagement metrics. The skill sends the link to LinkDigest and returns the available digest without downloading the video locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links are processed by LinkDigest, and digest text may be retained or shared through caching for the same public link.

Mitigation: Submit only public links and text you are comfortable sharing, and review the LinkDigest privacy policy.

Risk: Video processing and optional features consume credits, with cost varying by video length and selected options.

Mitigation: Set --max-credits to cap spending before submitting a link.

Risk: Using the optional mcp-remote connection adds a third-party client dependency.

Mitigation: Prefer the bundled script or direct HTTP integration, or pin a reviewed mcp-remote version.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-linkdigest-video-transcript)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest API](https://linkdigest.dev/api/v1/digest)
- [LinkDigest OpenAPI specification](https://linkdigest.dev/openapi.json)
- [ClawHub release page](https://clawhub.ai/jackchew7143/skills/linkdigest-video-transcript)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON digest with transcript segments, on-screen text, key points, and available video metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript timestamps are segment-level; on-screen text timestamps are approximate. Results may be partial when requested or returned as a summary.]

## Skill Version(s):

1.2.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
