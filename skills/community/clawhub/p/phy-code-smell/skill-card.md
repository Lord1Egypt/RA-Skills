## Description:

Static code smell detector for Python, JavaScript/TypeScript, Java, Go, and Ruby that identifies classic anti-patterns with severity ratings, line-level findings, and refactoring suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to scan source code for structural code-quality issues before refactoring, review, or CI enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and analyze source files under the selected project root and print code-derived findings.

Mitigation: Run it with an explicit --root scoped to the intended project or subdirectory, and avoid sharing reports from sensitive repositories without review.

Risk: Static analysis findings can be incomplete or imprecise and may lead to unnecessary refactoring if accepted without review.

Mitigation: Treat findings as review guidance and confirm each recommendation against the surrounding code before making changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-code-smell)
- [Canlah AI Homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style static analysis report with severity-ranked findings, line numbers, smell summaries, refactoring suggestions, and optional CI command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable thresholds and an optional CI fail gate for HIGH severity findings.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
