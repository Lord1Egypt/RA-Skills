## Description: <br>
Fetches live webpages through AgentPMT-hosted remote calls and returns webpage content as HTML, Markdown, or screenshots for real-time extraction and visual capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access live webpages through AgentPMT for research, content verification, competitive monitoring, RAG data extraction, and screenshot-based documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote browsing may expose private URLs, authenticated pages, account secrets, payment headers, or sensitive screenshots to the service. <br>
Mitigation: Use the skill only for approved browsing targets and do not submit sensitive URLs, authenticated pages, credentials, wallet keys, payment headers, or sensitive screenshots unless that processing is explicitly approved. <br>
Risk: Live web content can change or return unclear response shapes during production integrations. <br>
Mitigation: Fetch live schema or instructions before new production integrations and retry failed invocations only after correcting schema, authentication, or payment issues. <br>


## Reference(s): <br>
- [Live Web Page Browser ClawHub Page](https://clawhub.ai/agentpmt/skills/live-web-page-browser) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/live-web-page-browser) <br>
- [Generated Action Schema](schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples; remote tool responses can include HTML, Markdown, or screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The product action has no declared input parameters in the generated schema.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
