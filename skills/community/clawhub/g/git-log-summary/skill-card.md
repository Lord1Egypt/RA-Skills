## Description:

Generates Markdown Git commit summary reports with project information, branch details, commit totals, author statistics, recent commits, and commit-type counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wj-chitang](https://clawhub.ai/user/wj-chitang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to summarize local or remote Git repository history into Markdown reports for documentation, review, and sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote repository wrapper can execute unintended commands from crafted option values.

Mitigation: Avoid untrusted or user-supplied option values for remote analysis until the eval-based invocation is fixed, and review wrapper changes before installation.

Risk: Generated Markdown reports can expose sensitive Git metadata such as paths, remote URLs, author identities, branch names, and commit messages.

Mitigation: Treat generated reports as sensitive, redact them before sharing, and choose output locations appropriate for the repository data.

Risk: Remote repository analysis clones repositories into the working environment.

Mitigation: Use a disposable working directory for remote analysis and remove cloned repositories unless retention is explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wj-chitang/skills/git-log-summary)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include repository paths, remote URLs, author identities, branch names, commit messages, commit counts, and generated timestamps.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
