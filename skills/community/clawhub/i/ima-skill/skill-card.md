## Description: <br>
Ima Skill helps agents manage IMA notes and knowledge bases through the IMA OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoe1209](https://clawhub.ai/user/zoe1209) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search, read, create, and append IMA notes, and to upload, link, search, and manage knowledge-base content in a user's IMA account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private notes, modify remote content, and upload selected files. <br>
Mitigation: Install only when the agent should access IMA notes and knowledge bases, and confirm the exact destination before uploads or appends. <br>
Risk: The skill uses user-provisioned Client ID, API key, and temporary COS credentials. <br>
Mitigation: Protect credentials, avoid logging or storing them, and send them only to the intended IMA or Tencent COS endpoints. <br>
Risk: Uploaded files or URLs may be sent to IMA or Tencent COS. <br>
Mitigation: Avoid uploading files or URLs that the user does not want sent to those services. <br>


## Reference(s): <br>
- [Ima Skill on ClawHub](https://clawhub.ai/zoe1209/ima-skill) <br>
- [IMA](https://ima.qq.com) <br>
- [IMA Agent Interface](https://ima.qq.com/agent-interface) <br>
- [Knowledge Base API Reference](knowledge-base/references/api.md) <br>
- [Notes API Reference](notes/references/api.md) <br>
- [Tencent COS Documentation](https://cloud.tencent.com/document/product/436/7778) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provisioned IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
