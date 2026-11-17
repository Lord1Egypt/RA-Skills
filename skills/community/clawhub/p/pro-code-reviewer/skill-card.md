## Description:

Review code against Android/iOS/TypeScript/Go/general rules, including local diffs, commits, branches, and GitHub or GitLab pull requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timeaground](https://clawhub.ai/user/timeaground)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to perform structured code reviews with severity-ranked findings across Android, iOS, TypeScript, Go, and general code changes. It is intended for pre-merge review of local diffs, staged changes, commits, branches, and remote pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read repository diffs and fetch GitHub or GitLab pull request content.

Mitigation: Install and use it only in repositories where sending code diffs to the reviewing agent and fetching PR content is acceptable.

Risk: Review-scope instructions may place user-supplied Git revisions, branch names, ranges, or commit counts into shell-style commands without validation.

Mitigation: Validate commit hashes, branch names, ranges, and commit counts, and prefer structured command arguments over shell-style interpolation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/timeaground/skills/pro-code-reviewer)
- [README](artifact/README.md)
- [General Review Rules](artifact/references/review-general.md)
- [Android Review Rules](artifact/references/review-android.md)
- [iOS Review Rules](artifact/references/review-ios.md)
- [TypeScript Review Rules](artifact/references/review-typescript.md)
- [Go Review Rules](artifact/references/review-go.md)
- [Skill Vetter Review Rules](artifact/references/review-skill-vetter.md)
- [Issue Tracker](https://github.com/TimeAground/code-reviewer/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown review report with severity-ranked findings, file locations, problem statements, and fix suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise code snippets and next-step guidance depending on review context.]

## Skill Version(s):

1.3.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
