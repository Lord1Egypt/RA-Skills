## Description:

OpenTask is a distributed task-management skill for querying and managing tasks assigned to OpenClaw containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let OpenClaw agents query pending OpenTask work, create and update tasks, record task outcomes, inspect logs, and integrate task checks into HEARTBEAT workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HEARTBEAT workflow can cause an agent to act on remote tasks without clear validation or user approval.

Mitigation: Enable automatic HEARTBEAT execution only for reviewed, allowed task types and require explicit approval for consequential actions.

Risk: The skill uses an API key to access the OpenTask service.

Mitigation: Use a narrowly scoped API key, restrict the trusted OpenTask service, and avoid storing secrets or sensitive personal data in task fields or results.

Risk: Remote API calls may expose task data or credentials if sent over an untrusted connection.

Mitigation: Require HTTPS for non-local OpenTask hosts and limit service access to trusted environments.

## Reference(s):

- [OpenTask API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/linux2010/skills/opentask-client)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OPENTASK_HOST, OPENTASK_API_KEY, and optional OPENTASK_BOT_NAME environment variables.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
