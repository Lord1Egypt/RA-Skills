## Description: <br>
PDF转Word converts PDF documents to Word (.docx) files through a local document-conversion workflow with task status checks, downloads, batch conversion, and conversion history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veilei](https://clawhub.ai/user/veilei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert uploaded PDF files into downloadable Word documents and to inspect the conversion task status, output, and history through the local conversion service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow calls an unauthenticated local document-conversion service that stores uploaded files and conversion history. <br>
Mitigation: Run the service only in a trusted local environment, keep it bound to localhost, and avoid uploading highly sensitive PDFs unless storage and retention behavior are understood. <br>
Risk: Broad document-conversion prompts may cause the agent to use conversion paths beyond the intended PDF-to-Word workflow. <br>
Mitigation: Use explicit PDF-to-Word requests and verify the selected conversion type before uploading or converting documents. <br>


## Reference(s): <br>
- [PDF转Word ClawHub release](https://clawhub.ai/veilei/pdf-to-word-vei) <br>
- [API 参考](references/api.md) <br>
- [系统架构](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Markdown] <br>
**Output Format:** [Markdown with API request examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for uploading PDFs, creating conversion tasks, polling status, downloading DOCX results, and viewing conversion history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
