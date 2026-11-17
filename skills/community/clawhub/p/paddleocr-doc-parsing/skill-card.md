## Description:

Extracts structured Markdown and JSON from PDFs and document images, including tables, formulas, figures, headers, footers, multi-column layout, and reading order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobholamovic](https://clawhub.ai/user/bobholamovic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to parse complex PDFs and document images into structured Markdown or JSON for downstream review, extraction, and automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents may contain sensitive content processed through the PaddleOCR service.

Mitigation: Avoid highly sensitive documents unless PaddleOCR service terms, data-handling expectations, and local environment controls are acceptable for the use case.

Risk: The skill requires a PaddleOCR access token.

Mitigation: Store PADDLEOCR_ACCESS_TOKEN in a managed secret store or protected environment variable, and avoid exposing it in prompts, logs, or shared shell history.

Risk: The paddleocr CLI package may change behavior across releases.

Mitigation: Use a pinned or reviewed paddleocr package version in controlled or production environments.

## Reference(s):

- [PaddleOCR Official API CLI Documentation](https://www.paddleocr.ai/latest/en/version3.x/inference_deployment/serving/paddleocr_official_api/cli.html)
- [ClawHub Skill Page](https://clawhub.ai/bobholamovic/skills/paddleocr-doc-parsing)
- [ClawHub Publisher Profile](https://clawhub.ai/user/bobholamovic)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON result structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the paddleocr CLI and PADDLEOCR_ACCESS_TOKEN; CLI options can save result JSON and related resource files.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
