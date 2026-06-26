## Description: <br>
Checks Claude Max plan usage by launching Claude Code, running `/usage`, and reporting session and weekly usage metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Claude Code users with Claude Max subscriptions use this skill to check current session and weekly usage limits from inside an agent workflow. It returns readable usage metrics and does not modify billing, subscription, or account settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches the local Claude CLI under the user's logged-in Claude account and exposes usage metrics to the agent session. <br>
Mitigation: Install only when that account context and usage visibility are acceptable, and review the generated command before execution. <br>
Risk: The skill is deprecated and depends on interactive terminal automation that may be brittle. <br>
Mitigation: Prefer the native Claude `/usage` command, ccusage CLI, or CC Usage MCP server when available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/openclaw-claude-usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text summary with usage metrics and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Claude Code CLI authentication and an expect-capable terminal session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
