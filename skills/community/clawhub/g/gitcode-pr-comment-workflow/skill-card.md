## Description:

GitCode PR review comment response workflow that accepts a PR link, fetches review comments, checks out the PR source branch locally, proposes modification plans based on review feedback, applies confirmed changes, and commits and pushes back to the source branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guitenbay](https://clawhub.ai/user/guitenbay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to respond to GitCode pull request review feedback by collecting review comments, confirming an implementation approach, drafting a design plan, applying approved code changes, pushing to the PR source branch, and optionally replying to unaddressed review comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles GitCode repository credentials and may expose tokens through persistent notes or command-line access_token query parameters.

Mitigation: Use a narrowly scoped GitCode credential, avoid storing tokens in MEMORY.md, and prefer authenticated CLI flows or non-query-token mechanisms where available.

Risk: The workflow can push commits or post PR replies to the wrong branch, repository, or discussion if destinations are not checked.

Mitigation: Confirm the local repository, source branch, push remote, branch target, and every PR reply destination before any external write operation.

Risk: The documented cleanup command can delete the entire temp directory and may remove unrelated work if reused outside the intended workspace.

Mitigation: Restrict cleanup to workflow-owned temporary files and skip blanket temp directory deletion when the directory may contain unrelated files.

## Reference(s):

- [GitCode API Reference](references/gitcode-api.md)
- [gitcode CLI](https://github.com/codeasier/gitcode-cli)
- [ClawHub Skill Page](https://clawhub.ai/guitenbay/skills/gitcode-pr-comment-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, diffs, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary markdown or JSON workflow files and requires user confirmation before modifying files, pushing commits, or posting PR replies.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
