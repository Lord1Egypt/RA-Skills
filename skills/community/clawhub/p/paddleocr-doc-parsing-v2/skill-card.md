## Description:

Parse documents using PaddleOCR's API. Supports both sync and async modes for images and PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiotec](https://clawhub.ai/user/hiotec)

### License/Terms of Use:


## Use Case:

Developers and document-processing teams use this skill to parse image and PDF documents through a configured PaddleOCR API endpoint and receive structured OCR and layout output for downstream review or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents, document URLs, and API tokens can be sent to configured PaddleOCR or Baidu endpoints.

Mitigation: Use trusted HTTPS endpoints, avoid confidential or regulated files unless approved, and protect and scope PADDLEOCR_ACCESS_TOKEN.

Risk: Async mode follows a result URL provided by the OCR service.

Mitigation: Enable async processing only with approved endpoints and review the configured service behavior before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hiotec/skills/paddleocr-doc-parsing-v2)
- [PaddleOCR Official Website](https://www.paddleocr.com)
- [PaddleOCR API Documentation](https://ai.baidu.com/ai-doc/AISTUDIO/Cmkz2m0ma)
- [PaddleOCR GitHub Repository](https://github.com/PaddlePaddle/PaddleOCR)
- [PaddleOCR Quota Documentation](https://ai.baidu.com/ai-doc/AISTUDIO/Xmjclapam)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash examples and JSON OCR results that can include extracted Markdown document text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured PaddleOCR endpoints and an access token; sync mode prints JSON or writes it to a file, while async mode polls for service-hosted results.]

## Skill Version(s):

1.0.4 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
