## Description:

Generates Conventional Commits-compatible Git commit messages by analyzing repository diffs, project commit conventions, monorepo scopes, and optional split-commit groupings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hash-panda](https://clawhub.ai/user/hash-panda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze staged or unstaged Git changes, detect project commit-message conventions, infer scopes, and prepare commit messages or split-commit suggestions for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-changing Git commands can stage or commit unintended files.

Mitigation: Run in dry-run mode first and manually review the generated commit message and file list before allowing git add or git commit.

Risk: The npx fallback can auto-download an unpinned Bun runtime.

Mitigation: Prefer a locally installed trusted Bun binary and avoid the npx fallback when reviewing or using the skill.

Risk: Untrusted diffs or unusual filenames can make generated file operations harder to review safely.

Mitigation: Inspect repositories with untrusted changes carefully and verify staged paths before executing commit commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hash-panda/skills/panda-git-commit)
- [Project homepage](https://github.com/hash-panda/panda-skills#panda-git-commit)
- [Conventional Commits reference](references/conventional-commits.md)
- [Commit types reference](references/commit-types.md)
- [Convention detection reference](references/convention-detection.md)
- [Monorepo detection reference](references/monorepo-detection.md)
- [EXTEND.md configuration reference](references/extend-schema.md)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/zh-hans/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON analysis plus plain-text or Markdown commit-message guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file lists, inferred commit type and scope, convention metadata, split-commit suggestions, and optional raw diff output.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
