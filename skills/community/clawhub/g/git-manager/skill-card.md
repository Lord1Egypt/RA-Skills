## Description:

Execute common Git operations such as status, commit, push, pull, branch management, PR creation, merge, stash, log, and diff with dry-run support and structured output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyico](https://clawhub.ai/user/liyico)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run common Git repository workflows, including status checks, commits, pushes, pulls, branch management, merges, stashes, logs, and diffs. It is intended for controlled workspaces where Git actions can be reviewed and audited.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged entry point can execute unescaped user input through a shell.

Mitigation: Use only in tightly controlled workspaces, review commands before execution, prefer dry-run mode for planned changes, and do not grant access to repositories where injected or unintended commands would be costly.

Risk: The entry point delegates work to a hard-coded executable outside the reviewed package.

Mitigation: Do not rely on the stated safety checks until the executable path and implementation are packaged, reviewed, and argument handling avoids shell interpolation.

Risk: Git operations can change repository history or publish code to remotes.

Mitigation: Avoid use with sensitive credentials or high-value repositories unless repository permissions, protected branches, and human review gates are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyico/skills/git-manager)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON results and concise text guidance for Git command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw Git output, changed files, commit SHA, branch name, errors, and dry-run previews.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
