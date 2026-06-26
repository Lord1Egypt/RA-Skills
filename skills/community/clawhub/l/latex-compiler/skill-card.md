## Description: <br>
Compile LaTeX documents to PDF using pdflatex, xelatex, or lualatex with template support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willamhou](https://clawhub.ai/user/willamhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to compile LaTeX source strings, preview PDFs, and start from common LaTeX templates through a local compilation service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate local LaTeX compilation container. <br>
Mitigation: Review the referenced container setup before use, confirm the localhost port binding, and keep the service local-only. <br>
Risk: LaTeX source is sent to a service that the user may not have audited. <br>
Mitigation: Avoid compiling highly sensitive documents through the service unless the container and its runtime configuration have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/willamhou/latex-compiler) <br>
- [Prismer project](https://github.com/Prismer-AI/Prismer) <br>
- [Prismer LaTeX container source](https://github.com/Prismer-AI/Prismer/tree/main/docker/base) <br>
- [Prismer base Dockerfile](https://github.com/Prismer-AI/Prismer/blob/main/docker/base/Dockerfile) <br>
- [Prismer development Docker Compose](https://github.com/Prismer-AI/Prismer/blob/main/docker/docker-compose.dev.yml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON tool results containing PDF paths, base64 PDF data, logs, errors, warnings, and LaTeX template content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated PDFs are stored inside the local container; preview output can return a base64-encoded PDF.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
