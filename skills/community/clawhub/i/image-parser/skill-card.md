## Description:

Parse text and coordinates from images with SoMark (character/word/line positions on original image). Ideal for OCR-first image understanding where location matters. Requires SoMark API Key (SOMARK_API_KEY).

This skill is ready for commercial/non-commercial use.

## Publisher:

[soul-code](https://clawhub.ai/user/soul-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Image Parser to extract OCR text with bounding-box coordinates from receipts, invoices, forms, screenshots, and photographed documents for precise field extraction and location-aware automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and the SoMark API key are sent to a third-party service.

Mitigation: Use the skill only for images approved for upload to SoMark and keep the key in SOMARK_API_KEY instead of chat or command history.

Risk: The skill suggests making Image Parser a persistent default for future image text extraction.

Mitigation: Add the CLAUDE.md default rule only after deciding that future image OCR should route through this third-party service.

Risk: OCR coordinates and extracted text may be incomplete or incorrect for difficult images.

Mitigation: Review the *.text_bbox.json output before using it for field extraction, automation, or decisions that depend on exact location.

## Reference(s):

- [Image Parser on ClawHub](https://clawhub.ai/soul-code/skills/image-parser)
- [SoMark](https://somark.tech)
- [SoMark parse API endpoint](https://somark.tech/api/v1/parse/sync)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON and Markdown OCR output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOMARK_API_KEY; primary parsed output is *.text_bbox.json with text, bbox, page, and role fields.]

## Skill Version(s):

0.1.2 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
