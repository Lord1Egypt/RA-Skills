## Description: <br>
Use when the user mentions Jira issues, asks about tickets, wants to create, view, or update issues, check sprint status, or manage their Jira workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and project contributors use this skill to interact with Jira through natural language while drafting, viewing, updating, transitioning, assigning, and commenting on issues. It helps the agent choose an available Jira backend, show proposed actions, and require approval before ticket modifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent operating through an authenticated Jira account, so mistaken or overbroad actions could change tickets or notify watchers. <br>
Mitigation: Review commands or tool calls before approval, fetch current issue state before changes, and keep Jira credentials least-privileged. <br>
Risk: Jira tickets can contain secrets, private code, security findings, customer data, or internal URLs that may be copied into broadly visible tickets. <br>
Mitigation: Confirm visibility before moving sensitive information, avoid placing credentials or sensitive findings into ticket fields, and preserve access boundaries. <br>
Risk: Jira content can be untrusted input, including text that resembles shell commands or instructions. <br>
Mitigation: Treat fetched ticket content as data, use safe quoting or file-based input for CLI commands, and avoid automated transmission of Jira data to external URLs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/jira-hardened) <br>
- [jira CLI project](https://github.com/ankitpokhrel/jira-cli) <br>
- [Jira safety evaluation](https://faberlens.ai/explore/jira) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Jira CLI commands, MCP tool-call guidance, and ticket text drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses authenticated Jira CLI or Atlassian MCP tools when available; changes should be reviewed and approved before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
