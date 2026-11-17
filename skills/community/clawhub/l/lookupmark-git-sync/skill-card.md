## Description:

Manage whitelisted Git repositories from chat for status, log, diff, fetch, pull, and push operations with confirmation required for write commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lookupmark](https://clawhub.ai/user/lookupmark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and synchronize a configured allowlist of local Git repositories from an agent chat workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can pull or push configured repositories using the user's Git credentials when --confirm is supplied.

Mitigation: Keep ~/.config/git-sync/repos.json limited to intended repositories and require explicit human approval before an agent adds --confirm.

Risk: A broad or incorrect repository allowlist can expose unintended local repositories to git status, fetch, pull, or push actions.

Mitigation: Review the configured repository list before installation and after changes, and remove any path the agent should not manage.

## Reference(s):

- [Git CLI](https://git-scm.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations report repository status and history; write operations require the helper's --confirm flag.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
