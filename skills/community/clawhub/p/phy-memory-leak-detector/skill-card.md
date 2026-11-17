## Description:

Static memory leak pattern scanner for Node.js, Python, Go, and Java that reports common leak patterns and can guide optional local Node.js heap-diff confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan Node.js, Python, Go, and Java codebases for memory leak patterns, review suggested fixes, and optionally confirm suspected Node.js leaks with local heap profiling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional runtime profiling can execute unpinned npm tools and local load tests.

Mitigation: Pin clinic and autocannon through a lockfile-managed test environment before running heap profiling or load tests.

Risk: Runtime heap profiling and load tests may affect production services or expose sensitive local sessions.

Mitigation: Use the skill for static analysis first, and run runtime confirmation only in an isolated test environment against non-sensitive services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-memory-leak-detector)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with findings, severity summaries, code examples, fixes, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static analysis output with optional local Node.js heap profiling guidance]

## Skill Version(s):

1.0.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
