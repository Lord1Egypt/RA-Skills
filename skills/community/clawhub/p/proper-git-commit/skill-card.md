## Description:

Smart git commit with remote sync, amend intelligence, and conventional commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugogu](https://clawhub.ai/user/hugogu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent inspect Git changes, synchronize with the remote branch, decide whether to amend or create a new conventional commit, and optionally push when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically rebase, stage files broadly, amend commits, and push when requested.

Mitigation: Review the staged file list and diff before execution, and require explicit approval for rebase, broad staging, amend, and push steps.

Risk: Broad staging could include secrets or files that were not intended for the commit.

Mitigation: Inspect `git status --porcelain`, staged diffs, and untracked files before committing; exclude secret-bearing files such as `.env`, private keys, and credential files.

Risk: Generated commit footers may disclose agent or model metadata in repository history.

Mitigation: Confirm the generated footer matches project policy before committing or pushing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks and conventional commit text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May alter Git state when executed by an agent with shell access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
