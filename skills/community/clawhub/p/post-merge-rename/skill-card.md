## Description:

Post-merge branch renaming. Appends --merged-YYYY-MM-DD to preserve history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to identify branches merged into main and rename them with a dated --merged-YYYY-MM-DD suffix while preserving branch history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete old remote branch refs even though its documentation says it never deletes branches.

Mitigation: Review before installing or running in shared repositories; use --dry-run first and avoid production automation until the deletion behavior is explicit and verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/post-merge-rename)
- [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text terminal output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rename local branches, push new branch names, and delete old remote branch refs unless --dry-run is used.]

## Skill Version(s):

1.9.72 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
