## Description: <br>
Fill standard legal agreement templates such as NDAs, cloud service agreements, and SAFEs, produce signable DOCX files, and optionally send agreements for electronic signature via DocuSign. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to collect agreement fields, fill standard legal templates, generate DOCX agreements, and optionally send reviewed documents for signature. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agreement templates, field values, signer details, and authorization data may contain confidential or legally sensitive information. <br>
Mitigation: Prefer the local CLI path for offline filling, and use the hosted MCP or DocuSign signing flow only when the user accepts sending that data to those services. <br>
Risk: Generated agreements may have legal significance or may include compliance representations that require real-world confirmation. <br>
Mitigation: Require user review before signing, ask for explicit confirmation before setting compliance representation fields to true, and consider attorney review for important agreements. <br>
Risk: DocuSign signing requires OAuth authorization and may transmit filled agreement contents and signer contact information. <br>
Mitigation: Use the Open Agreements OAuth flow only when a tool reports missing authorization, avoid requesting raw DocuSign credentials, and confirm the user wants to send the document for signature. <br>
Risk: Installing or running the CLI can fetch package code from npm. <br>
Mitigation: Use the pinned `open-agreements@0.7.4` package path described by the artifact and avoid unpinned `@latest` installs. <br>


## Reference(s): <br>
- [Open Agreements repository](https://github.com/open-agreements/open-agreements) <br>
- [Open Agreements npm package](https://www.npmjs.com/package/open-agreements) <br>
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp) <br>
- [Open Agreements setup page](https://usejunior.com/developer-tools/open-agreements) <br>
- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/open-agreements) <br>
- [Template filling execution workflow](artifact/template-filling-execution.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command snippets and file paths or download links for generated DOCX agreements.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a hosted MCP service, local CLI, or preview-only path; local CLI filling can avoid third-party data transfer except DocuSign signing.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
