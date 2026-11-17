## Description:

Advanced local vision infrastructure for agents when built-in image tools are unavailable or unreliable, supporting batch image analysis, structured JSON output, screenshot and UI understanding, character and style classification, retryable workflows, and resilient image-processing pipelines backed by GMNCODE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[io2077](https://clawhub.ai/user/io2077)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep image-analysis workflows functional when a built-in image tool is unavailable or needs more control. It supports batch processing, structured JSON vision results, screenshot and UI analysis, and reusable fallback workflows for team agent systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill is marketed as local while uploading complete user-supplied images to an external GMNCODE endpoint without clear consent or privacy disclosure.

Mitigation: Before use, confirm that each image is acceptable to send to GMNCODE, especially screenshots, documents, internal tools, credentials, or personal data; prefer an explicitly consent-gated or local-only workflow for sensitive use cases.

Risk: The skill depends on a GMNCODE_API_KEY and external API availability for vision analysis.

Mitigation: Configure credentials through the runtime environment, restrict access to the key, and document fallback behavior for API failures or unavailable routes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/io2077/skills/local-gmncode-vision-pro)
- [Go-to-market notes](references-go-to-market.md)
- [GMNCODE Responses API endpoint](https://gmncode.cn/v1/responses)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, code, guidance]

**Output Format:** [Markdown guidance and strict JSON vision-analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured JSON results include summary, detected_entities, style, confidence, and uncertainty_notes; batch mode returns one result object per image.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
