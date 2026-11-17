## Description:

Parse complex PDFs and document images with MinerU through either the hosted MinerU API or the local open-source MinerU runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[focusshang](https://clawhub.ai/user/focusshang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to extract layout-aware Markdown, OCR text, formulas, and artifact paths from PDFs and document images with MinerU. It supports hosted API parsing for MinerU service workflows and local runtime parsing when documents should stay on the local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API mode handles credentials and uploads selected documents to the MinerU API.

Mitigation: Install only if you trust the MinerU API endpoint, use session-only tokens where possible, and prefer --mode local for sensitive files.

Risk: A custom MINERU_API_BASE_URL can direct documents and credentials to an unexpected endpoint.

Mitigation: Avoid custom MINERU_API_BASE_URL values unless you fully control the endpoint.

Risk: Generated outputs, downloaded archives, and extracted artifacts are written to local paths.

Mitigation: Set an explicit download directory and review generated artifact paths before sharing or retaining outputs.

## Reference(s):

- [MinerU OCR Local & API on ClawHub](https://clawhub.ai/focusshang/skills/mineru-ocr-local-api)
- [MinerU project homepage](https://github.com/opendatalab/MinerU)
- [MinerU API docs](https://mineru.net/apiManage/docs#/standard/openapi_v4)
- [MinerU output files documentation](https://opendatalab.github.io/MinerU/api/output_files/)
- [Output schema reference](references/output_schema.md)
- [httpx package](https://pypi.org/project/httpx/)
- [httpx repository](https://github.com/encode/httpx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON envelope with Markdown document text and saved artifact paths; user-facing responses are Markdown with relevant paths, excerpts, or summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save JSON envelopes, downloaded ZIP archives, extracted Markdown, middle JSON, content lists, and local MinerU artifact paths.]

## Skill Version(s):

1.1.4 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
