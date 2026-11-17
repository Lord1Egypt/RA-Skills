## Description:

Provides online OCR for image files and image URLs through the OCR.space API without requiring Tesseract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhi-collab](https://clawhub.ai/user/wangzhi-collab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and automation users use this skill to extract text from local image files, PDFs, PIL images, or image URLs through a Python API or command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, image URLs, and extracted text may be sent to or processed by OCR.space.

Mitigation: Use only with content approved for third-party OCR processing; avoid secrets, IDs, medical, financial, legal, and internal-only documents unless that processing is approved.

Risk: Extracted text may be cached locally by default when the CLI enables the .ocr_cache directory.

Mitigation: Run with --no-cache for sensitive content, or store cache files in an approved location and remove them after use.

Risk: Private OCR.space API keys passed directly on the command line may be exposed through shell history or process listings.

Mitigation: Avoid passing private API keys directly on shared systems; use an approved secret-handling workflow when available.

Risk: The artifact declares Python package usage but does not provide pinned dependency versions.

Mitigation: Install in a virtual environment and pin reviewed dependency versions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhi-collab/skills/online-ocr-skill)
- [OCR.space OCR API Documentation](https://ocr.space/ocrapi)
- [OCR.space Parse Image API Endpoint](https://api.ocr.space/parse/image)

## Skill Output:

**Output Type(s):** [text, JSON, files]

**Output Format:** [Plain text or JSON returned by Python methods, printed to stdout, or written to an output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language code, OCR engine, output path, JSON mode, cache directory, and no-cache controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
