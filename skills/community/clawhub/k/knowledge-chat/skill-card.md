## Description: <br>
Knowledge Chat 知识库对话助手 - 支持连接外部知识库、语义搜索、上下文对话、图片/附件理解。具备思考进度提示、Markdown渲染、后续建议、向量索引构建等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franksteinwen007-git](https://clawhub.ai/user/franksteinwen007-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and knowledge-base operators use this skill to connect external knowledge systems, run semantic searches, and support contextual chat over domain-specific documents and uploaded media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, retrieved knowledge content, uploaded images, and files may be sent to external AI or knowledge-base APIs. <br>
Mitigation: Use the skill only with data that your organization permits to leave the local environment, and avoid confidential documents or screenshots unless explicitly approved. <br>
Risk: API credentials are required for external services. <br>
Mitigation: Use scoped API keys from environment variables or a secrets manager, rotate them as needed, and do not hard-code secrets into skill files or prompts. <br>
Risk: Configured endpoints may route data to unintended external systems. <br>
Mitigation: Verify knowledge-base and AI API endpoints before use, and restrict access to trusted service URLs. <br>


## Reference(s): <br>
- [Knowledge Chat ClawHub Release](https://clawhub.ai/franksteinwen007-git/knowledge-chat) <br>
- [Knowledge Base API Integration Guide](references/api_patterns.md) <br>
- [Knowledge Chat Connector Reference](references/kb_connector.py) <br>
- [Shared Skill Link](https://xiaping.coze.site/skill/4dd4f1c0-d0d8-4f66-9ca2-588583beba92) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON examples, Python code, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include retrieved knowledge snippets, source references, follow-up questions, API configuration guidance, and commands for setup or connector use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
