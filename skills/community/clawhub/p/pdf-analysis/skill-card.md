## Description: <br>
PDF Analysis helps agents inspect PDF files with MinerU and return structured content that preserves layout, headings, tables, images, formulas, and document hierarchy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, data analysts, and document processing teams use this skill to analyze PDF structure and extract readable content from local PDFs or PDF URLs. It is suited to quick document inspection as well as fuller extraction workflows that need tables, formulas, OCR, page ranges, or multiple output formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs or PDF URLs may be processed by MinerU, which can expose confidential, regulated, or internal-only document content outside the agent environment. <br>
Mitigation: Use this skill only with documents approved for MinerU processing, and avoid confidential, regulated, or internal-only PDFs unless organizational policy allows it and the user understands where content, URLs, and outputs may be sent or stored. <br>
Risk: Full extraction depends on a MinerU token and local CLI installation, so misconfigured credentials or untrusted installs can affect reliability and account security. <br>
Mitigation: Install mineru-open-api from the documented package source, keep MINERU_TOKEN in the environment or MinerU auth store rather than in prompts or files, and review generated output before relying on it. <br>


## Reference(s): <br>
- [PDF Analysis ClawHub page](https://clawhub.ai/mzlzyca/pdf-analysis) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU project](https://github.com/opendatalab/MinerU) <br>
- [MinerU API token management](https://mineru.net/apiManage/token) <br>
- [mineru-open-api CLI package](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; MinerU can produce Markdown, HTML, JSON, LaTeX, DOCX, or files in an output directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mineru-open-api CLI. The MINERU_TOKEN environment variable is required for full extraction, while flash extraction supports smaller quick reads without a token.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
