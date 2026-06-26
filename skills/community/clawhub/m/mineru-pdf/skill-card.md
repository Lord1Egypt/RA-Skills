## Description: <br>
Parse PDF documents with MinerU MCP to extract text, tables, and formulas, with multiple backends including MLX-accelerated inference on Apple Silicon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Etoile04](https://clawhub.ai/user/Etoile04) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing users use this skill to extract structured Markdown, tables, formulas, and related files from PDFs and supported image formats. It supports direct persistent output and MinerU MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local documents are processed by mcp-mineru and MinerU components. <br>
Mitigation: Install only when comfortable with that processing path, and isolate or pin the external package when handling sensitive PDFs. <br>
Risk: The included test helper can execute unintended local code if run with crafted filenames or page values. <br>
Mitigation: Prefer parse.py or the scoped MCP setup, and avoid running test.sh with filenames or page values from untrusted sources. <br>


## Reference(s): <br>
- [MinerU MCP repository](https://github.com/TINKPA/mcp-mineru) <br>
- [ClawHub skill page](https://clawhub.ai/Etoile04/mineru-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files, extracted image files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a local PDF path, output directory, backend selection, page range, and table or formula recognition options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
