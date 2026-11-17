## Description:

Image analysis using multimodal vision models for describing images, extracting text, analyzing visual content, comparing images, and answering visual questions across JPG, PNG, GIF, and WebP inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cntuang](https://clawhub.ai/user/cntuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect supplied images, extract OCR text or structured fields, compare visuals, and answer questions about screenshots, documents, charts, forms, receipts, and photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images may contain receipts, business cards, forms, screenshots, IDs, medical records, credentials, or confidential business documents.

Mitigation: Use the skill only on images the agent is intended to inspect, and redact or limit extraction when full details are unnecessary.

Risk: Vision analysis can misread visual details, OCR text, charts, UI states, or extracted structured fields.

Mitigation: Review extracted text, structured data, and image conclusions before relying on them in downstream decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cntuang/skills/image-vision)

## Skill Output:

**Output Type(s):** [text, markdown, structured data, guidance]

**Output Format:** [Natural-language analysis, markdown summaries, and structured key-value extraction when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-image and multi-image analysis prompts; artifact evidence notes up to 20 images and automatic resizing for large images.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
