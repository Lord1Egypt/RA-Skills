## Description: <br>
Generates Conventional Commits-compatible Git commit messages, detects monorepo scopes, and can suggest splitting changes into multiple commits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hash-panda](https://clawhub.ai/user/hash-panda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill in Git repositories to inspect local diffs, detect project commit conventions and scopes, and generate or apply compliant commit messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Git diffs, recent commit messages, and repository configuration where it is invoked. <br>
Mitigation: Use it only in repositories whose contents are appropriate for agent review, and avoid staging secrets before use. <br>
Risk: Generated commit messages, EXTEND.md updates, split recommendations, or proposed commits may be inaccurate or unintended. <br>
Mitigation: Review generated messages, configuration changes, staged file groups, and any git commit action before accepting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hash-panda/panda-git-commit) <br>
- [Project homepage](https://github.com/hash-panda/panda-skills#panda-git-commit) <br>
- [Commit Types](references/commit-types.md) <br>
- [Convention Detection](references/convention-detection.md) <br>
- [Conventional Commits](references/conventional-commits.md) <br>
- [EXTEND Schema](references/extend-schema.md) <br>
- [Monorepo Detection](references/monorepo-detection.md) <br>
- [Conventional Commits specification](https://www.conventionalcommits.org/zh-hans/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with commit messages, split recommendations, summaries, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write EXTEND.md configuration during initialization or refresh workflows and may run git commit after user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
