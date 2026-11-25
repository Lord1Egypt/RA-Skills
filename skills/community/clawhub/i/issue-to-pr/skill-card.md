## Description:

Guides an agent through reproducing a GitHub issue, making and verifying a minimal fix, and preparing a pull request that follows repository conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ydx3906](https://clawhub.ai/user/4ydx3906)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to investigate and fix a GitHub issue in a local repository, verify the change against a baseline, and prepare a pull request with evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command does not pin the installer or skill revision, so fetched content could change.

Mitigation: Review the resolved skill contents before installation and use a pinned revision when the installer supports it.

Risk: Security analysis is incomplete because some referenced paths could not be resolved.

Mitigation: Review the complete skill package, including its referenced files, before installing or running it.

## Reference(s):

- [Project repository](https://github.com/4yDX3906/issue-to-pr)
- [ClawHub skill page](https://clawhub.ai/4ydx3906/skills/issue-to-pr)
- [PR evidence template](references/pr-evidence.md)
- [Run state schema](references/state.schema.json)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Markdown, Guidance]

**Output Format:** [Repository changes, verification artifacts, and a Markdown pull request report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a resumable run-state file, test evidence, and a pull request URL.]

## Skill Version(s):

1.4.0 (source: frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
