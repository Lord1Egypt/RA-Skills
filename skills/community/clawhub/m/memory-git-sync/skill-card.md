## Description:

Automates backup of the OpenClaw workspace to a remote Git repository, with large-file exclusions, Git configuration validation, and sync conflict handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vemec](https://clawhub.ai/user/vemec)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to back up and synchronize a Git working tree with a configured origin remote by staging, committing, pulling, and pushing changes through a Bash script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync script can stage, commit, and push the current Git working tree to origin without an explicit confirmation prompt.

Mitigation: Run `git status` before execution, confirm secrets and private files are ignored, and add a preview plus confirmation step before use in sensitive repositories.

Risk: The skill requires write access to the repository and credentials for the configured origin remote.

Mitigation: Confirm the origin URL, use a credential helper or SSH key with appropriate scope, and run it only in repositories intended for backup.

Risk: Automatic pull behavior can stop on conflicts or merge remote changes before pushing.

Mitigation: Review branch state before syncing and resolve conflicts manually before rerunning the script.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/vemec/skills/memory-git-sync)
- [Publisher profile](https://clawhub.ai/user/vemec)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and structured shell log output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and git; the script can commit and push repository changes to origin.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
