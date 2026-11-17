## Description:

OpenClaw skill auditing tool for scanning skills across security, performance, and quality rules before installation or release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill reviewers use this skill to inspect OpenClaw, ClawHub, GitHub, or third-party skills for security red flags, quality issues, performance concerns, and CI release gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner flaws could let unsafe skills appear acceptable in CI or machine-readable reports.

Mitigation: Treat results as advisory, manually review target skill instructions and excluded files, and do not rely on verdict_code or CI exit code alone.

Risk: Severity-cap or engine-class metadata may affect how findings are presented.

Mitigation: Review capped and uncapped severity information, including original_severity, before trusting an installation decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zuoyunlai/skills/lz-skill-vetter-20260819)
- [Original Skill Vetter Fork Source](https://clawhub.ai/spclaudehome/skills/skill-vetter)
- [Audit Protocol](references/audit_protocol.md)
- [Patterns Reference](references/patterns.md)
- [Output Format Reference](references/output_format.md)
- [Rules Documentation](references/_rules_documentation.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable text reports, JSON audit reports, and CI-oriented shell exit codes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports severity filtering and exit codes 0, 1, and 2 for CI workflows.]

## Skill Version(s):

2.1.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
