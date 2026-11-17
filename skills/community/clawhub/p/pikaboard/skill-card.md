## Description:

PikaBoard helps agents interact with a local PikaBoard task management API to create, update, list, and manage kanban tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angelstreet](https://clawhub.ai/user/angelstreet)

### License/Terms of Use:


## Use Case:

Developers and agent operators use PikaBoard to connect agents to a PikaBoard kanban/task API, assign each agent to a board, and create, list, or update tasks during work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation runs mutable external Node code during npm install and build steps.

Mitigation: Review before installing, run setup from a sandbox or low-privilege account, and verify the upstream repository revision before executing install or build commands.

Risk: Bearer tokens may be handled in plaintext environment files or copied into agent-facing documentation.

Mitigation: Avoid putting the bearer token in TOOLS.md or shared files, and protect backend/.env with restrictive permissions.

Risk: Agents can create or update tasks on the wrong board if board IDs are misconfigured.

Mitigation: Confirm board IDs before allowing task creation or updates, and operate only on the assigned board unless explicitly directed.

## Reference(s):

- [PikaBoard ClawHub skill page](https://clawhub.ai/angelstreet/skills/pikaboard)
- [PikaBoard repository from install metadata](https://github.com/angelstreet/pikaboard)
- [API documentation pointer](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with shell, environment, and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; uses PIKABOARD_API, PIKABOARD_TOKEN, AGENT_NAME, and optional board environment configuration.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
