## Description: <br>
Provides Perplexity web-grounded question answering, deep research, reasoning, and web search through OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to ask web-grounded questions, run deeper Perplexity research, perform step-by-step reasoning, and retrieve ranked web search results through OneKey Gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and prompts are sent to OneKey Gateway and Perplexity, and the scripts may use a shared demo key when no user key is configured. <br>
Mitigation: Set a private DEEPNLP_ONEKEY_ROUTER_ACCESS key, avoid submitting secrets or confidential data, and review third-party dependencies before sensitive use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AI-Hub-Admin/perplexity-onekey-gateway) <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Agent Router Documentation](https://deepnlp.org/doc/onekey_agent_router) <br>
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent) <br>
- [Skills Marketplace](https://www.deepnlp.org/store/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and markdown-style text with citations, snippets, URLs, and dates depending on the selected tool.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports message payloads, query payloads, recency filters, domain filters, search context sizing, reasoning effort, and optional thinking-stripping parameters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
