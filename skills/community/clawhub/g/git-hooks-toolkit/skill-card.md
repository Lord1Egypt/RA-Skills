## Description:

Generate, install, and manage Git hooks with pre-built templates for linting staged files, enforcing commit conventions, blocking debug statements, preventing large files, formatting code, protecting branches, running tests before push, and installing dependencies after merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, preview, install, inspect, and remove repository Git hooks that enforce common commit, push, formatting, and dependency workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that the remove command can delete files outside normal Git hooks when given unsafe hook names.

Mitigation: Review before installing and do not run the remove command with anything other than a standard Git hook name until path validation is fixed.

Risk: Installed hooks may persist in a repository and alter commit, push, merge, formatting, testing, and dependency workflows.

Mitigation: Use only in repositories where persistent Git hook behavior is intended, and preview templates before installation.

Risk: The post-merge dependency template can run package-manager commands after merges when lockfiles change.

Mitigation: Avoid the install-deps template unless automatic package-manager execution is acceptable for the repository.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnnywang2001/skills/git-hooks-toolkit)
- [Publisher Profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated Git hook scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write executable Git hook files into a repository when the user runs the included script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
