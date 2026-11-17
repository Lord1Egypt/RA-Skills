## Description:

Git Helper supports safe Git workflows for status checks, staging, Conventional Commit messages, pushes, pulls, rebases, logs, diffs, and branch operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougchambes](https://clawhub.ai/user/dougchambes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use Git Helper to perform common Git repository tasks with consistent checks, commit message conventions, and safeguards around history-changing operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive Git commands can discard local work or rewrite repository history if approved carelessly.

Mitigation: Review branch state and command intent before reset, rebase, hard reset, or force push operations; require explicit permission for destructive actions.

Risk: Force pushes and rebases can disrupt shared branches.

Mitigation: Use safer workflows such as status checks, backup branches, and force-with-lease only when the user confirms the branch is safe to rewrite.

## Reference(s):

- [Git Workflows Reference](references/workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline Git commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
