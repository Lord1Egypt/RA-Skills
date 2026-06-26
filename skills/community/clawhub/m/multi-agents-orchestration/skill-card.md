## Description: <br>
Defines how OpenClaw teams use backend sub-agent spawning and optional Discord mentions to coordinate multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cchaojiejes](https://clawhub.ai/user/cchaojiejes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators configuring OpenClaw use this skill to choose between backend orchestration, Discord-visible agents, and hybrid deployments, then apply the documented configuration and troubleshooting patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wildcard sub-agent permissions can grant broader agent-to-agent access than intended. <br>
Mitigation: Replace wildcard permissions in examples with named allowlists for the agents that should collaborate. <br>
Risk: Discord bot tokens and bindings can expose agents in unintended guilds or channels. <br>
Mitigation: Scope bot tokens, guild allowlists, channel permissions, and bindings to the required Discord surfaces only. <br>
Risk: Background sub-agent work may be difficult to review if approval and logging expectations are not defined. <br>
Mitigation: Document when background work requires approval and keep logs for delegated sub-agent activity. <br>
Risk: Bot-to-bot mentions can create visible cross-agent interactions that are not part of the core orchestration flow. <br>
Mitigation: Leave bot-to-bot mentions disabled unless the workflow explicitly requires public multi-agent collaboration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cchaojiejes/multi-agents-orchestration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, JavaScript, shell, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for configuring OpenClaw agents and Discord bindings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
