## Description:

Launch non-blocking Claude Code headless tasks from slash command dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edxi](https://clawhub.ai/user/edxi)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to launch asynchronous Claude Code tasks for a named project and task, with optional Agent Teams behavior when requested by the prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start long-lived local Claude Code agents that act on project workspaces.

Mitigation: Install only where callers and runtime environments are controlled, and use strict allowlists for project and task names.

Risk: Prompts, logs, metadata, and results may be stored locally in plaintext under configured result and log directories.

Mitigation: Keep result and log directories private and avoid sending sensitive prompts unless local plaintext storage is acceptable.

Risk: Permission modes can increase the authority of background Claude Code runs.

Mitigation: Avoid bypassPermissions and review permission-mode configuration before enabling the skill.

## Reference(s):

- [Claude Code headless mode documentation](https://code.claude.com/docs/en/headless)
- [Claude Code Agent Teams documentation](https://code.claude.com/docs/en/agent-teams)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration]

**Output Format:** [Plain text launch summary with log and result paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts long-running local background processes and writes task logs and results to configured directories.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
