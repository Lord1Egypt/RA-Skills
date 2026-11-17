## Description:

Guides an interactive Git bisect to identify the commit that introduced a reproducible regression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to narrow a reproducible regression between known good and bad Git revisions, classify intermediate commits, and restore the original checkout after bisecting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bisect changes the local checkout and can disrupt uncommitted work.

Mitigation: Start with a clean worktree or stash or commit changes, and run git bisect reset when finished.

Risk: Optional bisect automation runs a local test script across historical commits.

Mitigation: Review and trust the script before using git bisect run.

## Reference(s):

- [Git documentation](https://git-scm.com/doc)
- [Git Bisect Coach on ClawHub](https://clawhub.ai/hmahmadcs/skills/git-bisect-coach)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with Git command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive good/bad/skip prompts and a first-bad-commit summary]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
