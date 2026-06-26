## Description: <br>
统一 IMA OpenAPI 技能，支持笔记管理、知识库操作、文件上传、网页添加和内容搜索。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dayofyear](https://clawhub.ai/user/dayofyear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users and agents use this skill to manage IMA notes and knowledge bases: search, read, create, and append notes; list and search knowledge bases; add URLs or notes; and upload files through the documented multi-step flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generic Node API helper can send IMA credentials to an arbitrary URL if invoked with a full URL. <br>
Mitigation: Prefer the narrower notes and knowledge-base scripts; when using the generic helper, pass only expected relative IMA API paths and avoid full URLs. <br>
Risk: Write operations can affect the wrong note or knowledge base if IDs are mistaken. <br>
Mitigation: Confirm target note IDs, knowledge-base IDs, and upload destinations before create, append, add, upload, or delete actions. <br>
Risk: IMA API keys and COS temporary credentials are sensitive secrets. <br>
Mitigation: Use least-privilege IMA credentials, keep config files private, and treat COS temporary credentials as secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dayofyear/ima-skill-ref) <br>
- [IMA homepage](https://ima.qq.com) <br>
- [IMA OpenAPI credentials](https://ima.qq.com/agent-interface) <br>
- [Knowledge base API reference](knowledge-base/references/api.md) <br>
- [Notes API reference](notes/references/api.md) <br>
- [Permissions and security notes](PERMISSIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY, or matching files under ~/.config/ima.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
