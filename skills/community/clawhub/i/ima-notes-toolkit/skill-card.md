## Description: <br>
Ima Notes Toolkit helps an agent route IMA OpenAPI requests for personal notes and knowledge-base operations, including note search, note creation, note updates, file uploads, web link imports, and knowledge-base search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiyongwang](https://clawhub.ai/user/ruiyongwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage IMA notes and knowledge bases through the official IMA OpenAPI. It supports workflows such as searching notes, creating or appending note content, uploading files, importing web links, and searching or browsing knowledge bases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private IMA notes and knowledge bases using user-provisioned credentials. <br>
Mitigation: Install it only when that access is acceptable, and store credentials in tightly permissioned environment variables or configuration files. <br>
Risk: Bundled notes debug scripts may expose account identifiers or private note data in logs. <br>
Mitigation: Avoid running the debug scripts unless needed for troubleshooting, and treat any debug output as sensitive. <br>
Risk: Appending to an existing note changes user content and may be difficult to undo. <br>
Mitigation: Require an explicit target note before append operations and ask the user to confirm when the target is ambiguous. <br>
Risk: Incorrect text encoding can corrupt note content during write operations. <br>
Mitigation: Validate or convert note titles and content to UTF-8 before write API calls, and use explicit UTF-8 byte bodies in PowerShell 5.1. <br>


## Reference(s): <br>
- [IMA](https://ima.qq.com) <br>
- [IMA OpenAPI credential page](https://ima.qq.com/agent-interface) <br>
- [Notes API reference](notes/references/api.md) <br>
- [Knowledge Base API reference](knowledge-base/references/api.md) <br>
- [Tencent Cloud COS request signature documentation](https://cloud.tencent.com/document/product/436/7778) <br>
- [ClawHub skill page](https://clawhub.ai/ruiyongwang/ima-notes-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, API calls, markdown] <br>
**Output Format:** [Markdown with inline shell commands, JSON request bodies, and API workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or execute authenticated IMA API requests using user-provisioned credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
