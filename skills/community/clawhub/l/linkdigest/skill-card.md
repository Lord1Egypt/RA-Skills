## Description:

Read a social media link that returns nothing useful when fetched — Xiaohongshu (小红书), Douyin (抖音), TikTok, YouTube, X, or an ordinary web page. Returns the transcript, the on-screen text, a description of every image, the caption and the metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI agents can use this skill to read social posts and videos when a normal page fetch does not expose their content. It returns text such as transcripts, on-screen text, image descriptions, captions, and metadata for follow-up questions or summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links may contain access tokens or private information, and sending them to an external service may expose that information.

Mitigation: Review links for tokens or private details and get informed consent before submitting them.

## Reference(s):

- [LinkDigest on ClawHub](https://clawhub.ai/jackchew7143/skills/linkdigest)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Readable digest in Markdown by default, or structured JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transcripts, OCR text, image descriptions, captions, metadata, and optional translation or post breakdowns.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
