## Description:

Proofreader helps agents check drafts for typos, grammar issues, style consistency, document consistency, readability, and proofreading report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to guide proofreading of Chinese or English drafts, including typo, grammar, style, consistency, readability, and full-report checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated generic local data-storage CLI that can retain user text in plaintext without clear documentation.

Mitigation: Review the package before installation, remove or disable the generic storage script if it is not needed, and avoid using it with sensitive drafts unless local retention is clearly scoped and disclosed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/proofreader)
- [Publisher profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown proofreading prompts, reports, and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled generic CLI may write local plaintext log or data files when used directly.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
