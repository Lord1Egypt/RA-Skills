## Description:

OCR for PowerPoint (.pptx) presentations with scanned or image-embedded slide content using MinerU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract searchable text from image-heavy, scanned, or screenshot-based PowerPoint presentations. It helps route .pptx OCR work through MinerU with token-based authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR may send presentation content to an external MinerU service.

Mitigation: Avoid confidential presentations unless organizational policy allows third-party OCR processing.

Risk: The MINERU_TOKEN credential is required for extraction and could be exposed if mishandled.

Mitigation: Keep the token scoped and protected, and prefer reviewed or pinned mineru-open-api versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/pptx-ocr)
- [MinerU homepage](https://mineru.net)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU API token page](https://mineru.net/apiManage/token)
- [Publisher profile](https://clawhub.ai/user/mzlzyca)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; MinerU OCR output may be stdout text or files in an output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mineru-open-api binary and MINERU_TOKEN for OCR extraction.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
