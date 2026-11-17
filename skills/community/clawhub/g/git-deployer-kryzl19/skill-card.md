## Description:

Push static site content to GitHub Pages or another git-backed host by cloning the target repository, copying files, committing with a timestamp, and force-pushing to a branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to publish local static site output to GitHub Pages or another git remote when they want a direct git-based deployment flow instead of a CI pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment flow force-pushes to the target branch and can overwrite remote Git history.

Mitigation: Use it only with repositories and branches you are willing to overwrite, avoid shared or protected branches, and prefer confirmation or --force-with-lease for safer operation.

Risk: The script uses a predictable temporary clone path under /tmp.

Mitigation: Use a private unpredictable temporary directory and inspect existing clones before deploying.

Risk: Untrusted site directories may contain repository metadata or hooks that affect automated commits.

Mitigation: Use only trusted site directories, reject embedded .git content in site input, and disable Git hooks during automated commits.

Risk: Incorrect remote or branch arguments may deploy content to the wrong destination.

Mitigation: Validate the remote URL and branch before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports success or failure details, including commit hash, remote URL, branch, and push status when deployment completes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
