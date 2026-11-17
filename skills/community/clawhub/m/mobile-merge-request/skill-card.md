## Description:

Guides the merge request and pull request workflow for mobile teams: branch naming, Conventional Commits, small and stacked MRs, self-review, rebase vs merge, safe conflict resolution for lockfiles, project.pbxproj and version catalogs, MR descriptions with screenshots and rollback, and reviewer etiquette.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT

## Use Case:

Mobile developers and reviewers use this skill to prepare GitHub pull requests or GitLab merge requests, from branch and commit hygiene through conflict resolution, review responses, and a clear release description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested global Git settings affect every repository, and rebases or force pushes can alter shared history if used on the wrong branch.

Mitigation: Prefer repository-local settings when appropriate, verify the target branch and remote before history changes, and review proposed rewrites and pushes before approving them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ahmadhussain0335/skills/mobile-merge-request)
- [Publisher profile](https://clawhub.ai/user/ahmadhussain0335)
- [Git commands](artifact/references/git-commands.md)
- [Conflict resolution](artifact/references/conflicts.md)
- [MR template and reviewer etiquette](artifact/references/mr-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown prose, checklists, merge request templates, and inline Git commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts examples and checklist items to the repository and change details provided by the user.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
