## Description:

Control OpenCode directly via the Agent Client Protocol (ACP). Start sessions, send prompts, resume conversations, and manage OpenCode updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[studio-hakke](https://clawhub.ai/user/studio-hakke)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to control OpenCode through ACP, including starting sessions, sending prompts, resuming prior sessions, and checking or updating OpenCode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Update guidance includes unsafe remote installer execution and overbroad process-killing instructions.

Mitigation: Review update steps before running them; independently verify installer sources and stop only the intended OpenCode processes.

Risk: The session-resume flow can expose prior OpenCode conversation history to the current agent context.

Mitigation: Resume sessions only when prior conversation history is appropriate for the current task and user.

## Reference(s):

- [Agent Client Protocol docs for agents](https://agentclientprotocol.com/llms.txt)
- [OpenCode ACP skill repository](https://github.com/bjesuiter/opencode-acp-skill)
- [OpenCode latest releases](https://github.com/anomalyco/opencode/releases/latest)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands and JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes polling, session tracking, resume, cancellation, and update workflows.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
