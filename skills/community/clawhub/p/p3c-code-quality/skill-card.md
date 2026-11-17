## Description:

Reviews Java code against Alibaba P3C code-quality standards, including naming, exception handling, concurrency, database, OOP, security, and unit-testing rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohalo](https://clawhub.ai/user/ohalo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Java engineering teams use this skill to review Java files or directories against Alibaba P3C rules and produce a categorized Markdown quality report before commits, regression testing, or release review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a generated Markdown report inside the repository, which may appear in commits unintentionally.

Mitigation: Review the configured report path and generated files before committing repository changes.

Risk: Static rule matching and code-quality diagnostics can produce false positives or suggestions that do not fit project context.

Mitigation: Have a Java maintainer review reported severity, code locations, and suggested fixes before changing production code.

Risk: The skill reads the Java files or directories selected for inspection.

Mitigation: Scope the requested code path to the intended source tree and avoid including unrelated sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ohalo/skills/p3c-code-quality)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown report with categorized findings, severity counts, code locations, and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a report under doc/{business}/测试报告/{test_content}/ when used as described.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
