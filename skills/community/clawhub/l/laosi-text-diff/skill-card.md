## Description:

文本对比 - 对比两段文本差异，逐行diff，高亮变更，支持side-by-side和unified格式输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and technical writers use this skill to compare text, code, configuration, documents, or program output and identify added, removed, or changed lines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Comparing files exposes selected file contents to the agent performing the diff.

Mitigation: Use explicit file selections and avoid sensitive files unless their contents are intended for analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-text-diff)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or plain text diff output with unified or side-by-side sections and change statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-selected files for comparison; no hidden execution, persistence, network use, or unrelated data access was identified in the security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
