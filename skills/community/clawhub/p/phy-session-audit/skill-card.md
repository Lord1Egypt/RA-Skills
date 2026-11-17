## Description:

Phy Session Audit helps agents scan web application source code for session and cookie security weaknesses aligned to OWASP A07:2021, including missing cookie flags, token exposure, session fixation, CSRF gaps, localStorage credential storage, missing timeouts, weak session IDs, and broad cookie domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit application repositories for common session management and cookie configuration weaknesses before release or during CI review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic scanner findings may be incomplete or include false positives, especially for framework-specific Koa, Fastify, FastAPI, Rails, and CSRF patterns.

Mitigation: Use the skill as a lightweight audit helper and manually verify findings before treating them as confirmed vulnerabilities or release blockers.

Risk: Scanner output can include file paths, line numbers, and short code snippets from scanned repositories.

Mitigation: Run the skill only on intended code paths and review CI logs or shared reports before exposing them outside the project team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-session-audit)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples and plain-text scanner findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings may include file paths, line numbers, severities, CWE mappings, and remediation suggestions.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
