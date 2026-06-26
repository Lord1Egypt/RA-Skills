## Description: <br>
Parses complex PDFs and document images with MinerU through either the hosted MinerU API or a local open-source MinerU runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Focusshang](https://clawhub.ai/user/Focusshang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract layout-aware Markdown and text from PDFs or document images, choosing hosted MinerU API mode for service-backed parsing or local mode when documents should remain on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode can upload PDFs or images to the hosted MinerU service. <br>
Mitigation: Use --mode local for confidential documents, and use API mode only when uploading the document to MinerU is acceptable. <br>
Risk: OCR outputs and downloaded archives may be saved on the local filesystem. <br>
Mitigation: Review artifact paths returned by the skill and delete saved OCR artifacts when they are no longer needed. <br>
Risk: API mode depends on trusted MinerU endpoint and token configuration. <br>
Mitigation: Keep MINERU_API_TOKEN private and only use trusted MINERU_API_BASE_URL values. <br>


## Reference(s): <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU API Documentation](https://mineru.net/apiManage/docs#/standard/openapi_v4) <br>
- [MinerU Output Files Documentation](https://opendatalab.github.io/MinerU/api/output_files/) <br>
- [MinerU OCR Local API Output Schema](references/output_schema.md) <br>
- [httpx Python Package](https://pypi.org/project/httpx/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [JSON envelope with extracted Markdown text, artifact paths, and optional command or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save OCR results, downloaded archives, extracted Markdown, and local MinerU artifact paths depending on mode and flags.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
