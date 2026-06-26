## Description: <br>
调用久吾智能体API进行文本或文件分析处理，支持按智能体名称、文档编号和文本内容或文件列表发起合同评审、需求评审、文档审查等智能分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[05u](https://clawhub.ai/user/05u) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to route contract text, document files, and requirements materials to a Jiuwu review service for AI-assisted review opinions. Typical tasks include contract clause analysis, requirements review, document review, and issue analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends document text, uploaded files, and a bearer token to a hard-coded plain-HTTP internal endpoint. <br>
Mitigation: Install only when 192.168.1.213:5000 is the intended trusted Jiuwu service, use a limited and revocable token, and confirm the network path is approved. <br>
Risk: Submitted materials may contain confidential, regulated, or third-party information. <br>
Mitigation: Avoid sending sensitive documents unless the organization has approved the Jiuwu service and its data-handling practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/05u/jiuwu-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text review output with JSON API responses surfaced through a command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JIUWU_CORE_TOKEN and access to the configured Jiuwu service endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
