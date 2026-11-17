## Description:

Use this skill for Indices CLI operations, including authentication, tasks, runs, and secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsaphel](https://clawhub.ai/user/itsaphel)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to ask an agent for Indices CLI commands and guidance for authentication, task management, run execution, and secret management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and secret values can be exposed if placed directly in command arguments or shared command history.

Mitigation: Prefer interactive login, secure secret prompts, or stdin-based secret input, and avoid embedding real credentials in commands.

Risk: Delete operations and commands using --yes can remove Indices resources without an interactive confirmation step.

Mitigation: Review delete commands and any --yes flag with the user before execution.

Risk: Task creation payloads could request fully autonomous execution.

Mitigation: Do not allow task creation payloads that set is_fully_autonomous to true.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for credential handling, secret binding, manual task completion, and confirmation before delete operations.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
