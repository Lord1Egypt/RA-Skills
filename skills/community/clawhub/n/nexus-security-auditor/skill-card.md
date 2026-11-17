## Description:

Red/Blue team security audit with CVE scanning, OWASP analysis, and penetration testing recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuwanito](https://clawhub.ai/user/shuwanito)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and authorized assessment teams use this skill to review target context for OWASP Top 10 issues, CVEs, Auth/AuthZ concerns, WAF rules, and security headers, then produce severity-ranked findings and improvement proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Penetration-testing guidance could be misused against systems the user is not authorized to assess.

Mitigation: Use the skill only for systems where the user has explicit authorization, and treat any live scanning or exploitation as dependent on separate approved tools and permissions.

Risk: Security recommendations may be incomplete or incorrect without corroboration.

Mitigation: Review the generated findings, require the documented minimum of two independent sources for cross-validation, and confirm changes before deployment.

## Reference(s):

- [Project homepage](https://github.com/Shuwanito/SkillsMP/tree/main/.claude/skills/nexus-security-auditor)
- [ClawHub skill page](https://clawhub.ai/shuwanito/skills/nexus-security-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or structured text with severity classifications, confidence scores, citations, and prioritized recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are classified as CRITICAL, HIGH, MEDIUM, LOW, or INFO; proposals include impact, effort, and priority scores.]

## Skill Version(s):

2.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
