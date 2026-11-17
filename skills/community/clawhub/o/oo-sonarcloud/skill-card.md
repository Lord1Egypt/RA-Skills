## Description:

Use SonarQube Cloud to search projects and issues and retrieve code-health measures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search SonarQube Cloud projects and issues and review selected code-health measures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can trigger execution of unverified downloaded code; the remote installers were unavailable for inspection.

Mitigation: Review setup steps, install a verified CLI release yourself, and require approval before the agent executes a downloaded installer.

## Reference(s):

- [SonarQube Cloud](https://www.sonarsource.com/products/sonarqube/cloud/)
- [SonarQube Cloud Web API documentation](https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/web-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [SonarQube Cloud ClawHub release](https://clawhub.ai/oomol/skills/oo-sonarcloud)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project, issue, and code-health information returned for the requested search or read.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
