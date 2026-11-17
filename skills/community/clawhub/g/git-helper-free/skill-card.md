## Description:

Git辅助 helps agents support common Git workflows such as status checks, pull and push operations, branch management, and log review with Chinese-language interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to ask an agent for routine Git repository operations and concise status or change-log results. It is most useful in repositories where agent-assisted Git inspection and mutations are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward Git commands that change files, branches, remotes, or history.

Mitigation: Require explicit user confirmation before pull, push, branch mutation, write, remote, or history-changing commands are run.

Risk: The trigger scope is broad and loosely defined, so the skill may be invoked for repositories where Git mutations are not intended.

Mitigation: Use it only in repositories approved for agent-assisted Git work and prefer read-only status or log checks before any mutating action.

Risk: The artifact describes generic Git helper behavior and may not provide enough constraints for safe command construction.

Mitigation: Review proposed commands for repository path, branch, remote, and credential exposure before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-helper-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON-style summaries with inline shell commands when Git actions are proposed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe Git repository status, branch activity, pull or push results, logs, errors, and follow-up recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
