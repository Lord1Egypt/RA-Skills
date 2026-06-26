## Description: <br>
Paper Parser helps agents parse academic papers and research PDFs with MinerU, extracting structured content such as sections, formulas, tables, figures, and references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, graduate students, literature review tools, and academic content managers use this skill to parse PDFs or arXiv paper URLs with MinerU and extract structured paper content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MinerU token is required for extraction and could expose account access if shared or committed. <br>
Mitigation: Treat MINERU_TOKEN as a secret, configure it only in trusted environments, and avoid storing it in source files or logs. <br>
Risk: Private or sensitive documents may be processed through MinerU's CLI/API service. <br>
Mitigation: Use the service only for documents whose privacy and retention implications are acceptable for the user's environment. <br>


## Reference(s): <br>
- [MinerU](https://mineru.net) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU Open API CLI](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on the mineru-open-api CLI, token configuration, PDF inputs, and optional output directories.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
