## Description: <br>
PDF to HTML helps an agent convert local or URL-based PDF documents into HTML using the MinerU CLI service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and publishing workflows use this skill to turn PDFs into web-ready HTML while preserving document structure where MinerU supports it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external MinerU CLI package and service. <br>
Mitigation: Install the CLI only from trusted package sources and use it only where MinerU service use is approved. <br>
Risk: The MinerU token can grant access to extraction features if exposed. <br>
Mitigation: Use a dedicated MINERU_TOKEN and keep it out of shared files, prompts, logs, and committed configuration. <br>
Risk: PDF content may be sent through MinerU during conversion. <br>
Mitigation: Avoid processing confidential, regulated, or credential-bearing PDFs unless organizational policy approves that data path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzlzyca/pdf-to-html) <br>
- [MinerU Homepage](https://mineru.net) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>
- [MinerU Project](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers MinerU CLI installation, MINERU_TOKEN authentication, PDF inputs, HTML output, language hints, and page ranges.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
