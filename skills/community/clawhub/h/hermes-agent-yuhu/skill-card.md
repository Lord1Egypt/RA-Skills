## Description:

Complete guide to using and extending Hermes Agent, including CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and contributor workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oicqren](https://clawhub.ai/user/oicqren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to configure Hermes Agent, troubleshoot CLI and gateway workflows, spawn additional agent instances, and understand extension points for tools, skills, memory, profiles, and contribution work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release normalizes direct remote installer execution.

Mitigation: Review the remote installer before running it and prefer a controlled environment for installation or testing.

Risk: Approval bypass or yolo modes can allow powerful commands to run without normal confirmation.

Mitigation: Avoid approval-bypass modes except in controlled environments with clear rollback and monitoring.

Risk: Gateway, cron, persistent memory, credentials, and spawned-agent features can act across sessions and external services.

Mitigation: Scope credentials and platform access carefully, review long-running agent behavior, and disable features that are not needed.

## Reference(s):

- [Hermes Agent repository](https://github.com/NousResearch/hermes-agent)
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/)
- [Messaging platform docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)
- [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [Provider integrations guide](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference)
- [Slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands)
- [ClawHub skill page](https://clawhub.ai/oicqren/skills/hermes-agent-yuhu)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational guidance for local agents, gateway services, credentials, cron jobs, memory, profiles, tools, and spawned agent processes.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
