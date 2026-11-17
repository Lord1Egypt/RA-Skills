## Description:

Persistent task ledger for agent coordination. Plan multi-step work, checkpoint progress across session boundaries, and coordinate across multiple agents with project pool routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan multi-step work, checkpoint progress across sessions, and coordinate handoffs across one or more agents using the hzl CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes optional instructions for an always-on, network-reachable dashboard and service that can persist after logout.

Mitigation: Use only the basic hzl CLI unless the dashboard is explicitly needed; before enabling it, review host binding, authentication, token handling, service persistence, and how to stop or disable the service.

Risk: The skill documents gateway and cloud sync options that may involve remote endpoints and tokens.

Mitigation: Enable gateway or cloud sync only after confirming the endpoint, token storage, and authentication requirements; prefer verified or pinned package versions.

Risk: The artifact documents destructive commands that can delete task-ledger data without recovery.

Mitigation: Do not run force initialization or prune commands unless the user explicitly asks to delete data and understands there is no undo.

## Reference(s):

- [HZL homepage from ClawHub metadata](https://github.com/tmchow/hzl)
- [HZL product site](https://hzl-tasks.com)
- [ClawHub skill page](https://clawhub.ai/tmchow/skills/hzl)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the hzl CLI; installation options in ClawHub metadata include Homebrew package hzl and npm package hzl-cli.]

## Skill Version(s):

3.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
