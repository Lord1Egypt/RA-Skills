## Description: <br>
Guides OpenClaw agents in invoking the Claude Code CLI for code development, code review, bug fixing, automation, and Alibaba Cloud Bailian-compatible provider configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kotoriy](https://clawhub.ai/user/Kotoriy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to run Claude Code from OpenClaw for code review, refactoring, testing, bug fixing, commits, PR creation, and Alibaba Cloud Bailian-compatible Claude API configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claude Code workflows can make broad code changes and assist with commits or PR creation. <br>
Mitigation: Use plan or confirmation-oriented modes for sensitive repositories, review generated changes before applying them, and approve commits and PRs manually. <br>
Risk: MCP servers and third-party provider endpoints can expose repositories or credentials to external services. <br>
Mitigation: Add only trusted MCP servers, scope credentials to least privilege, and avoid plaintext API keys when a safer secret mechanism is available. <br>
Risk: The skill includes powerful CLI options such as permission skipping and automated execution. <br>
Mitigation: Reserve high-autonomy options for controlled environments and prefer explicit approval for file edits, shell commands, and network-connected tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kotoriy/openclaw-claude-code-bailian) <br>
- [Claude Code installer](https://claude.ai/install.ps1) <br>
- [Alibaba Cloud Bailian Claude-compatible endpoint](https://coding.dashscope.aliyuncs.com/apps/anthropic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell, JSON, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Claude Code CLI invocation patterns, permission-mode guidance, MCP examples, and provider configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
