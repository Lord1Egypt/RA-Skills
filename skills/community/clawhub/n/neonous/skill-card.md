## Description: <br>
Operate the Neonous AI agent platform to create agents, chat, manage tools, and run workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chesterchou](https://clawhub.ai/user/chesterchou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Neonous users use this skill to operate Neonous accounts from an assistant, including listing resources, chatting with agents, creating simple agents, running workflows, and checking billing or token status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad Neonous account-changing actions, including sharing artifacts, deleting content, resetting working memory, connecting Telegram bots, changing agents or MCP servers, and running workflows. <br>
Mitigation: Require explicit user confirmation before any sharing, deletion, reset, integration, configuration change, or workflow execution. <br>
Risk: API operations depend on NEONOUS_API_KEY and NEONOUS_URL, which could expose account access if mishandled. <br>
Mitigation: Verify NEONOUS_URL before use, protect the API key, avoid exposing it in responses or logs, and rotate it if disclosure is suspected. <br>
Risk: The security evidence flags insufficient guardrails for destructive and account-modifying actions. <br>
Mitigation: Prefer the Neonous web interface for complex or sensitive operations and review proposed API commands before execution. <br>


## Reference(s): <br>
- [Neonous homepage](https://neonous-ai.com) <br>
- [ClawHub skill listing](https://clawhub.ai/chesterchou/neonous) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown responses with curl and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEONOUS_API_KEY, NEONOUS_URL, curl, and jq for API operations.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
