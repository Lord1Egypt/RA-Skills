## Description: <br>
Standardizes cross-agent communication protocols for asking, collaborating with, or delegating work to another agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auberghan](https://clawhub.ai/user/auberghan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose the right communication pattern for cross-agent questions, one-way notifications, delegated background work, and sequential or parallel multi-agent coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-to-agent handoffs may expose sensitive user, business, or credential data if forwarded without review. <br>
Mitigation: Do not include passwords, API keys, private business data, or sensitive personal details in forwarded tasks unless the target agent and workspace are trusted. <br>
Risk: Using stale session keys can send work to the wrong or unavailable agent. <br>
Mitigation: Retrieve the current session key with sessions_list before sending or spawning agent work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/auberghan/openclaw-agent-comm) <br>
- [Skill source artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command examples and message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes timeout guidance, control directives, and error-handling templates for agent handoffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
