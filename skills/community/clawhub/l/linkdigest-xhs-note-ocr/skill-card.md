## Description:

Extracts Xiaohongshu note text, per-image OCR and descriptions, key points, tags, and engagement data through LinkDigest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill when a user shares a Xiaohongshu note and wants its caption, image text, descriptions, key points, tags, or engagement counts in a readable digest. It reads individual links and does not search, comment, or publish.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links and their results are handled by LinkDigest, results may be shared by link, and processing may involve third-party models.

Mitigation: Submit only content appropriate for this processing, remove unrelated personal text, and review the LinkDigest privacy policy.

Risk: API use can incur credit charges, and an exposed API key could be misused.

Mitigation: Keep LINKDIGEST_API_KEY private and use --max-credits to cap spending for a request.

Risk: The optional MCP bridge is not pinned to a version.

Mitigation: Prefer the bundled client or direct HTTP, or review and pin the MCP bridge before use.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-linkdigest-xhs-note-ocr)
- [LinkDigest API specification](https://linkdigest.dev/openapi.json)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest API key setup](https://linkdigest.dev/signin?ref=skill-linkdigest-xhs-note-ocr&next=/app/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-image OCR and descriptions, key points, tags, and a snapshot of engagement counts.]

## Skill Version(s):

1.2.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
