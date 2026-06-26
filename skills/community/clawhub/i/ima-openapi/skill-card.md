## Description: <br>
IMA OpenAPI helps agents manage IMA notes and knowledge bases, including searching, browsing, creating, and appending notes, uploading files, adding web pages, and searching knowledge-base content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxu41](https://clawhub.ai/user/jerryxu41) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with their IMA notes and knowledge bases through authenticated IMA OpenAPI workflows. It supports note search and editing, knowledge-base search and browsing, file uploads, web-page imports, and access to source content when the user has authorized credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify IMA notes and knowledge bases when supplied with user credentials. <br>
Mitigation: Install it only when that access is intended, keep IMA credentials private, and confirm write, upload, or append operations before execution. <br>
Risk: The authenticated helper is broader than the documented note and knowledge-base workflows. <br>
Mitigation: Review requested API paths and options before use, and avoid custom endpoints or base URL overrides unless the endpoint is trusted. <br>


## Reference(s): <br>
- [IMA homepage](https://ima.qq.com) <br>
- [IMA Agent Interface](https://ima.qq.com/agent-interface) <br>
- [Knowledge Base API reference](knowledge-base/references/api.md) <br>
- [Notes API reference](notes/references/api.md) <br>
- [Tencent COS request signature reference](https://cloud.tencent.com/document/product/436/7778) <br>
- [ClawHub release page](https://clawhub.ai/jerryxu41/ima-openapi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and user-provisioned IMA OpenAPI credentials.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release evidence and artifact/meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
