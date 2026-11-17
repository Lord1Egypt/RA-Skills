## Description:

Assesses system performance indicators and security risks across response time, concurrency, resource use, OWASP Top 10 risks, and related dimensions, then produces quantitative conclusions and remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and security reviewers use this skill to structure performance testing, security assessment, penetration-test review, risk evaluation, and audit reporting for systems they are authorized to assess.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for system access details and may be used around credentials or customer data.

Mitigation: Use least-privilege test accounts, avoid privileged production secrets or customer data, and provide only the minimum context required for assessment.

Risk: The skill describes penetration and load testing workflows that can disrupt systems if used without clear authorization and scope.

Mitigation: Run testing only against authorized targets, prefer staging environments, and define scope, timing, rate limits, and rollback expectations before testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/performance-security-assessor)
- [Publisher profile](https://clawhub.ai/user/golngod)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown assessment reports with ratings, metric tables, risk lists, detailed findings, and remediation recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include performance ratings, security risk severity, affected scope, repair difficulty, and remediation priority when supported by user-provided system context.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
