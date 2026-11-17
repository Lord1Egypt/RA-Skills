## Description:

Git高级操作专业版 helps developers and engineering teams plan and execute advanced Git workflows such as sparse checkout, subtrees, submodules, rerere conflict reuse, cherry-picking, and repository history analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill for advanced Git operations in large or complex repositories, including monorepo optimization, shared-code management, conflict reuse, batch cherry-picking, and repository history analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested Git commands can change repository state, alter global Git configuration, push changes, or remove files when run in the wrong repository, branch, or path.

Mitigation: Confirm the target repository, branch, paths, remotes, and working-tree state before running commands such as rm -rf, git rm, git push, git config --global, merge, cherry-pick, or cache-clearing commands.

Risk: Conflict-reuse workflows such as rerere can repeat an incorrect prior resolution.

Mitigation: Review rerere diffs and run the project test or validation workflow before committing reused conflict resolutions; forget or clear incorrect rerere records when needed.

Risk: Submodule, subtree, and cross-repository migration commands depend on external repository access and correct remote selection.

Mitigation: Verify remote URLs, credentials, target branches, and intended ownership boundaries before fetching, pushing, or migrating commits across repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-workflows-tool-pro)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and optional structured JSON-style results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status, result, metadata, execution log, and error fields when presenting structured task results.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
