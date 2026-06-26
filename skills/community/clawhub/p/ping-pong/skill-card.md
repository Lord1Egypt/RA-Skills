## Description: <br>
Agent Ping-Pong guides a human-relayed workflow where OpenClaw specifies and reviews work while Codex or Claude Code implements changes through GitHub pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[highnoonoffice](https://clawhub.ai/user/highnoonoffice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical operators use this skill to coordinate two-agent coding work, with a human relaying structured handoff blocks between OpenClaw and a coding agent. It is intended for GitHub PR workflows that keep implementation in a sandbox, preserve review, and require explicit approval before merge or production porting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow describes sending handoff blocks to a fixed Telegram destination, which could expose work context or route messages to an unintended recipient. <br>
Mitigation: Use the skill only when you control the destination, remove or replace the hardcoded chat destination, and require explicit approval for each external send. <br>
Risk: The workflow requires GitHub personal access tokens for the participating agents. <br>
Mitigation: Use fine-grained, repo-limited tokens only, avoid broad or classic tokens, and scope each token to the minimum repositories and permissions needed. <br>
Risk: Clipboard handoff blocks can expose secrets or private business details to local processes or external messaging if copied into the workflow. <br>
Mitigation: Keep raw credentials and sensitive details out of handoff blocks; store credentials only in agent configuration and review blocks before relaying them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/highnoonoffice/ping-pong) <br>
- [Project homepage](https://github.com/highnoonoffice/agent-ping-pong) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured handoff blocks and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-stream agent guidance for repository setup, PR handoffs, review loops, and approval gates.] <br>

## Skill Version(s): <br>
2.8.1 (source: server release metadata; artifact frontmatter lists 2.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
