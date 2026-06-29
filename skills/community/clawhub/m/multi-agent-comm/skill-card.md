## Description: <br>
Multi-agent-comm guides OpenClaw agents through structured multi-agent communication, including subagent delegation, persistent sessions, ACP-based cross-agent messaging, task decomposition, and shared context strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncepuee](https://clawhub.ai/user/ncepuee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate OpenClaw agents through one-off delegation, long-running sessions, and ACP communication. It helps split work across multiple agents, pass required context, configure agent definitions, and collect results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Multi-agent sessions may expose shared workspaces, skills, environment variables, or session history to agents that should not receive them. <br>
Mitigation: Review which agents share those resources before use, keep API keys in a secure secret store, and avoid plaintext secrets in copied folders or configuration examples. <br>
Risk: Resuming an unfamiliar session can continue prior context or actions that the user did not intend to trust. <br>
Mitigation: Resume only sessions you recognize and prefer a fresh session for sensitive work. <br>


## Reference(s): <br>
- [ACP Setup Guide](references/acp-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/ncepuee/skills/multi-agent-comm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, command, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable scripts are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
