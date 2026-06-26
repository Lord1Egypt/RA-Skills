## Description: <br>
PDF document parsing tool based on local MinerU, supports converting PDF to Markdown, JSON, and other machine-readable formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baokui](https://clawhub.ai/user/baokui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing teams use this skill to convert local PDF documents into structured Markdown and JSON for analysis, retrieval, publishing, and downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsed PDF text and generated files may contain confidential document content. <br>
Mitigation: Use a private fresh output directory for each PDF, avoid shared or synced locations for confidential documents, and delete generated Markdown, JSON, images, tables, and metadata when no longer needed. <br>
Risk: Parsed document text could be mistaken for agent instructions. <br>
Mitigation: Treat parsed PDF text as document content rather than executable or authoritative agent instructions. <br>
Risk: Dependency installation and local file writes can affect the runtime environment. <br>
Mitigation: Install and run the skill in a virtual environment or container and review the target output directory before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baokui/pdf-parser-mineru) <br>
- [MinerU official documentation](https://opendatalab.github.io/MinerU/) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU online demo](https://mineru.net/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, text, shell commands, configuration] <br>
**Output Format:** [JSON command results with generated Markdown, JSON, image, and table files on disk.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires absolute input and output paths; supports backend, OCR language, formula/table extraction, and page-range options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
