## Description: <br>
Auto-generated skill for google-search tools via OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Google Search queries through OneKey Gateway and retrieve search results for automation or research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and payload fields are sent to OneKey Gateway and Google. <br>
Mitigation: Avoid sensitive or confidential search payloads unless that data sharing is approved for the deployment. <br>
Risk: The scripts include a shared demo API key fallback when DEEPNLP_ONEKEY_ROUTER_ACCESS is not set. <br>
Mitigation: Set DEEPNLP_ONEKEY_ROUTER_ACCESS to an owned key before normal, sensitive, or production use. <br>
Risk: The skill depends on third-party npm and Python packages. <br>
Mitigation: Review and pin the required packages in higher-trust environments before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AI-Hub-Admin/google-search-onekey-gateway) <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway Documentation](https://deepnlp.org/doc/onekey_agent_router) <br>
- [Google Custom Search API](https://www.googleapis.com/customsearch/v1) <br>
- [AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell examples and JSON search-result responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS for normal use; query, num, start, and return_fields control Google Search requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
