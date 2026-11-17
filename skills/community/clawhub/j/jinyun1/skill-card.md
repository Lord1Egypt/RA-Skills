## Description:

Reviews Go projects for security, performance, correctness, maintainability, and test coverage issues, and produces structured recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjypink1211](https://clawhub.ai/user/jjjypink1211)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review Go pull requests and services for security vulnerabilities, performance bottlenecks, correctness defects, maintainability issues, and test coverage gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes team-effectiveness analytics guidance that references fixed local repository paths, named contributors, a fixed branch, and an external dashboard.

Mitigation: Remove or replace hard-coded repository paths, contributor names, fixed branch, external dashboard URL, and token-based API guidance before use.

Risk: The skill can prompt access to additional repositories, employee metrics, or external services during team-effectiveness analysis.

Mitigation: Require explicit approval before using any repository, employee metric, access token, or external service beyond the code review requested by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jjjypink1211/skills/jinyun1)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Go Testing](https://go.dev/doc/testing)
- [Go Coverage](https://go.dev/blog/cover)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [DORA Metrics](https://dora.dev/)
- [SPACE Framework](https://queue.acm.org/detail.cfm?id=3454124)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review reports with prioritized issue lists, coverage tables, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated coverage.out and test-report.json when coverage analysis is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
