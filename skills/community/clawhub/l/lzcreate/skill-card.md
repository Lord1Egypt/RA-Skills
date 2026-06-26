## Description: <br>
Supports end-to-end Landing Zone migration from AWS, Alibaba Cloud, GCP, Huawei Cloud, and Azure to Tencent Cloud by using a remote MCP server to scan source cloud resources, fill migration surveys, generate design documents, and generate Terraform code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awaili](https://clawhub.ai/user/awaili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud architects, migration engineers, and developers use this skill to automate Tencent Cloud Landing Zone migration planning and implementation from supported source clouds. It helps discover source resources, complete migration surveys, generate design documentation, and produce Terraform for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for cloud credentials and sends credential-bearing files to a remote MCP server over plain HTTP. <br>
Mitigation: Use only a trusted MCP server and network path, prefer verified HTTPS or a self-hosted endpoint, and provide short-lived read-only credentials scoped to the exact accounts and regions needed. <br>
Risk: Credential-bearing sessions and generated migration artifacts may expose sensitive cloud information if mishandled. <br>
Mitigation: Keep session IDs private, rotate credentials after use, and review all generated documents and Terraform before applying or sharing them. <br>


## Reference(s): <br>
- [MCP API Reference](references/mcp_api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/awaili/lzcreate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts include Excel survey files, Markdown design documents, and Terraform code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses remote MCP sessions; review generated documents and Terraform before using them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
