## Description:

Verifies workspace state and staged changes as a read-only preflight. Use before commits or PRs to confirm staged set is clean and correct.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before commit, pull request, or release-note workflows to review repository status, staged and unstaged changes, and diff details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the skill as suspicious because some steps direct changes to files and Git state despite its read-only preflight description, and reported checks may not verify the staged changes or workspace state described.

Mitigation: Review commands before running them, avoid staging, unstaging, or other workspace changes without explicit approval, and independently confirm repository status and the diff.

Risk: The security scan is partial because a referenced local test path was missing.

Mitigation: Treat the review as incomplete until the referenced test path and the applicable checks are confirmed in the target repository.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-sanctum-git-workspace-review)
- [Sanctum project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown review notes with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes repository status and diff findings for downstream workflows.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
