## Description:

Provides access to Perplexity web-grounded question answering, research, reasoning, and search tools through OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Perplexity-backed tools for cited answers, deeper web research, step-by-step analysis, and ranked web search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports unpinned executable package installation.

Mitigation: Install in an isolated environment, avoid global installation, and pin dependency versions before operational use.

Risk: The security summary reports fallback to a shared gateway key when no user key is set.

Mitigation: Set DEEPNLP_ONEKEY_ROUTER_ACCESS to a user-controlled key and avoid sending sensitive prompts or internal data through the demo fallback key.

## Reference(s):

- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys)
- [OneKey MCP Router Doc](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway Doc](https://deepnlp.org/doc/onekey_agent_router)
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent)
- [Skills Marketplace](https://www.deepnlp.org/store/skills)
- [AI Agent A2Z Deployment](https://www.deepnlp.org/workspace/deploy)
- [GitHub AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-formatted tool responses with citations or search result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports recency filters, domain filters, search context sizing, reasoning effort, result limits, page token limits, and country selection depending on the selected tool.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
