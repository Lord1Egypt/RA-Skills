## Description:

Fact-checks news articles, social media posts, images, and videos for claims, manipulated media, deepfakes, out-of-context media, and misinformation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cliffyan28](https://clawhub.ai/user/cliffyan28)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to verify factual claims and assess image or video authenticity in any language. It routes text, image, and video inputs through evidence-search and media-analysis workflows and returns sourced verdicts with confidence scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External API paths and web-based fact checking may send claims, images, video-derived audio, or other user content to third-party services.

Mitigation: Use the skill only for content that can be shared externally, disable optional API paths for confidential material, and obtain consent before uploading private media.

Risk: Credential checks and optional API calls can expose API keys if commands print environment variable values.

Mitigation: Review and adjust credential-check commands so they test for key presence without printing secret values.

Risk: Local media processing uses shell commands and optional binaries such as ffmpeg, exiftool, c2patool, and whisper.

Mitigation: Run media analysis in a controlled environment, inspect generated commands before execution, and process only trusted local files.

Risk: Fact-checking results can be incomplete or misleading when web search evidence is unavailable, sparse, or low quality.

Mitigation: Require cited sources, preserve UNVERIFIED verdicts when evidence is insufficient, and apply human review before using reports in high-impact decisions.

## Reference(s):

- [Fact Checker Homepage](https://github.com/cliffyan28/fact-checker)
- [External API Reference](references/api_docs.md)
- [Text Verification Pipeline](references/text_pipeline.md)
- [Image Verification Pipeline](references/image_pipeline.md)
- [Video Verification Pipeline](references/video_pipeline.md)
- [Fact-Check Report JSON Schema](references/output_schema.json)
- [Google Fact Check Tools API](https://developers.google.com/fact-check/tools/api/reference/rest)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports by default, with JSON available on request and source URLs included for verdict evidence.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include per-claim or per-media verdicts, confidence scores, source attribution, status lines, and optional local media-processing command results.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
