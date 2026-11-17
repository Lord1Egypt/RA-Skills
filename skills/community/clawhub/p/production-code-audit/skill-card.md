## Description:

Deep-scans a codebase to understand its architecture and patterns, then produces a prioritized production-readiness audit across security, performance, quality, testing, logging, documentation, and related risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to audit codebases for production readiness, with prioritized findings across security, performance, architecture, quality, testing, and operational gaps. When explicitly requested, it can prepare branch-based remediation and PR-ready changes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expand from read-only audit reporting into broad codebase edits, branch or PR creation, dependency changes, infrastructure additions, or local test execution if used without explicit operator control.

Mitigation: Use read-only audit mode by default and require explicit confirmation before file edits, branch creation, PR creation, dependency changes, infrastructure additions, or local test execution.

Risk: Discovered secrets could be mishandled if an agent attempts automatic remediation.

Mitigation: Report secret locations without exposing values, review secret findings separately, and rotate credentials outside the skill.

## Reference(s):

- [Production Code Audit on ClawHub](https://clawhub.ai/solomonneas/skills/production-code-audit)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [SonarQube Quality Gates](https://docs.sonarqube.org/latest/user-guide/quality-gates/)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown audit reports with prioritized findings, optional code changes, and shell commands when fixes are explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity-ranked findings, file and line references, branch or PR workflow guidance, and test or verification notes.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
