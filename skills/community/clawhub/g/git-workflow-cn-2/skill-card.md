## Description:

Git工作流 helps Chinese-speaking developers manage Git branches, resolve merge conflicts, and prepare Conventional Commit messages for team workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill for Chinese-language Git workflow assistance, including branch management, merge-conflict handling, rollback and recovery guidance, and commit-message preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation language and destructive Git commands could lead to discarded work or rewritten history.

Mitigation: Limit use to explicit Git workflow requests, create a backup or inspect repository state first, and require clear user confirmation before reset --hard, clean -f/-fd, filter-branch, BFG deletion, reflog expiry, or aggressive gc.

Risk: Generated conflict-resolution or commit guidance may be incorrect for the repository's intent.

Mitigation: Review diffs, run relevant tests, and verify branch state before committing, merging, reverting, or pushing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-workflow-cn-2)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with Git command examples and structured JSON-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Git workflow recommendations, conflict-resolution steps, commit-message suggestions, and command snippets.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
