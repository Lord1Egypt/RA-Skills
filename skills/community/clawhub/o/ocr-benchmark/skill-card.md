## Description:

Multi-model OCR benchmark and comparison tool for running OCR on local images with Claude via Bedrock, Gemini via Google AI Studio, and optional PaddleOCR, then comparing accuracy, cost, and speed against human-verified ground truth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingfengli](https://clawhub.ai/user/yingfengli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation teams use this skill to benchmark OCR quality across supported model providers, score results against human-reviewed ground truth, and generate comparison reports for product packaging or document images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload user-selected images to cloud providers or a configured OCR endpoint, which may expose sensitive documents, product images, personal data, or regulated content.

Mitigation: Use only approved providers for the data being processed and avoid running the benchmark on sensitive or regulated images unless those providers are authorized.

Risk: A custom PaddleOCR endpoint may receive image data and an optional OCR token without strong endpoint validation.

Mitigation: Use a trusted HTTPS PaddleOCR endpoint, avoid setting PADDLEOCR_TOKEN for untrusted destinations, and review endpoint configuration before execution.

Risk: Generated OCR results and scores may be incorrect or misleading if model output is treated as ground truth.

Mitigation: Use human-verified ground truth and review benchmark outputs before relying on rankings or reports.

Risk: Installing runtime dependencies can affect the host Python environment.

Mitigation: Install in an isolated virtual environment with pinned or reviewed dependencies.

## Reference(s):

- [Model Registry](artifact/references/models.md)
- [Ground Truth Format](artifact/references/ground-truth-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON result files, scored terminal summaries, and optional PPTX reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-image per-model JSON files, scores.json, ranked terminal output, and optional presentation reports.]

## Skill Version(s):

2.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
