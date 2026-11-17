## Description:

Git基础工具免费版 provides Chinese-language guidance for core Git workflows, including repository setup, commits, branching, remote synchronization, history inspection, stash, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to receive Git command guidance for initializing repositories, staging and committing changes, managing branches, synchronizing remotes, reviewing history, and recovering changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run Git commands that alter repository state, history, remotes, or credentials.

Mitigation: Require the agent to show git status and relevant diffs, then ask for explicit confirmation before reset, clean, force push, branch or tag deletion, remote deletion, or credential changes.

Risk: Credential-storage guidance may lead to insecure persistent credential storage.

Mitigation: Prefer secure operating-system credential managers or SSH keys instead of credential.helper store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-essentials-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and INI code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an agent with command execution capability and Git 2.20+ for executable workflows.]

## Skill Version(s):

1.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
