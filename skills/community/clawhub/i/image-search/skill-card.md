## Description:

Visual image search using Google Lens via SerpAPI to identify objects, landmarks, products, plants, animals, artwork, logos, people, or other visual entities from an image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiaslee](https://clawhub.ai/user/tobiaslee)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent workflows use this skill to identify image contents, find visually similar or exact-match images, retrieve shopping results with prices, and request image provenance metadata. It can search by public image URL or local file path when a SerpAPI key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file searches can upload readable files up to 32 MB to third-party image hosts without runtime confirmation.

Mitigation: Prefer public image URLs and require explicit user confirmation before using local file paths, especially for private photos, screenshots, documents, or arbitrary user-provided paths.

Risk: Image searches send image URLs and related request data to external visual-search services.

Mitigation: Avoid submitting sensitive or confidential images unless the user has approved the external search and understands the data exposure.

## Reference(s):

- [ClawHub Image Search Skill](https://clawhub.ai/tobiaslee/skills/image-search)
- [SerpAPI](https://serpapi.com/)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured Markdown summaries by default, or raw JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPAPI_KEY; local file inputs may be uploaded to a third-party image host before search.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
