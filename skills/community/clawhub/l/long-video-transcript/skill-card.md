## Description:

Turns supported long-video links into timestamped transcripts, on-screen text, and concise summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users can submit supported public video links to receive a transcript, on-screen text, metadata, and key points for note-taking, study, or content review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default command settings may incur more credits than the advertised discounted transcript mode, and YouTube remains on full-tier billing.

Mitigation: Before paid use, explicitly choose transcript depth and set a max-credit limit; check the service documentation for YouTube pricing behavior.

Risk: Results may be cached and shared with other users who submit the same link.

Mitigation: Submit public video links only; do not send private or sensitive links.

Risk: The optional mcp-remote bridge adds a third-party executable dependency.

Mitigation: Prefer the bundled script or direct HTTP integration; review and pin mcp-remote before use.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-long-video-transcript)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest OpenAPI specification](https://linkdigest.dev/openapi.json)
- [LinkDigest MCP client repository](https://github.com/jcaiagent7143-ui/linkdigest-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON with transcript segments, on-screen text, metadata, and key points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript timestamps are segment-level; on-screen text timing is approximate.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
