## Description: <br>
Convert PDF documents to LaTeX source using MinerU, extracting text, formulas, and document structure for academic and technical documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, graduate students, academics, and technical writers use this skill to convert local or URL-hosted PDF documents into LaTeX for editing, reproduction, or reference. It is best suited for papers and documents with formulas, tables, scanned content, or complex layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents may be processed by MinerU's external service, which can expose confidential, proprietary, unpublished, or regulated documents to a third-party provider. <br>
Mitigation: Use the skill only with documents appropriate for MinerU processing, follow the provider's terms, and avoid sensitive PDFs unless the processing arrangement is acceptable. <br>
Risk: The skill requires a MINERU_TOKEN and installation of the mineru-open-api CLI. <br>
Mitigation: Protect the token, avoid committing it to files or logs, install the CLI from trusted package sources, and consider pinning the CLI version. <br>


## Reference(s): <br>
- [PDF to LaTeX on ClawHub](https://clawhub.ai/mzlzyca/pdf-to-latex) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, Code] <br>
**Output Format:** [Markdown with inline shell commands and LaTeX-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mineru-open-api CLI and a MINERU_TOKEN; LaTeX output is produced by MinerU extract with -f latex.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
