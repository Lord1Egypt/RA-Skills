## Description: <br>
WhoBot (呼波特) AI电话数字员工知识库，帮助 agents answer questions about WhoBot company information, product capabilities, core technologies, industry use cases, team, compliance, and related topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whobot-ai](https://clawhub.ai/user/whobot-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer Chinese and English questions about WhoBot, including product positioning, technical differentiators, industry scenarios, business metrics, team, funding, and compliance. The bundled MCP server can expose the knowledge base through local stdio tools for WhoBot-specific Q&A. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional HTTP MCP server could be exposed to untrusted networks. <br>
Mitigation: Prefer the default stdio MCP setup and do not expose the HTTP server outside trusted environments. <br>
Risk: External sync or update workflows could change the knowledge base used for answers. <br>
Mitigation: Review any external GitHub sync or update workflow before running it. <br>
Risk: Real deployments involving call recordings, healthcare calls, CRM updates, or webhooks can create consent, retention, access-control, and regulatory obligations. <br>
Mitigation: Handle consent, retention, access control, and regulatory review separately before production deployment. <br>


## Reference(s): <br>
- [WhoBot Knowledge Base](references/knowledge.md) <br>
- [WhoBot Homepage](https://www.whobot.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/whobot-ai/openclaw-whobot-skill) <br>
- [OpenClaw MCP Config Schema](https://docs.openclaw.ai/schemas/mcp-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown responses through MCP tools, plus JSON MCP configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers are grounded in the bundled WhoBot knowledge base and FAQ search; default local setup uses stdio transport.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
