## Description:

Linux Cron Panel helps agents manage Linux crontab jobs through a local web API, including installation checks, task creation, editing, deletion, immediate runs, toggling, and log viewing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdmywm3](https://clawhub.ai/user/wdmywm3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install or connect to Linux Cron Panel and manage Linux scheduled tasks through its local HTTP API. It is intended for creating scripts, registering cron jobs, running tasks on demand, toggling task state, and checking execution logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may clone and run unverified third-party code that remains active as a user-level service.

Mitigation: Require explicit approval before installation, prefer a pinned and verified release, and document how to disable and remove the service.

Risk: The skill can create, delete, toggle, and immediately run scheduled commands on the user's machine.

Mitigation: Review each proposed cron expression and command before execution, especially destructive, privileged, or network-facing tasks.

## Reference(s):

- [Linux Cron Panel repository](https://github.com/wdmywm3/linux-cron-panel)
- [Linux Cron Panel ClawHub page](https://clawhub.ai/wdmywm3/skills/linux-cron-panel)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with shell commands, JSON API examples, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands that install a user-level service or create, modify, run, and delete scheduled tasks.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
