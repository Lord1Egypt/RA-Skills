## Description:

Detects ghost references in code, including unset environment variables, stale config keys, deprecated API endpoints, and local-only file paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect repositories for stale assumptions after refactors, before deployments, during onboarding, or during architecture review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect configuration, environment, CI/CD, or deployment files that contain sensitive values.

Mitigation: Run it only on repositories approved for agent inspection, and provide sanitized environment examples or key-only extracts instead of real secrets, tokens, passwords, production connection strings, or secret manifests.

## Reference(s):

- [Phantom Limb on ClawHub](https://clawhub.ai/jcools1977/skills/phantom-limb)
- [Publisher profile](https://clawhub.ai/user/jcools1977)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with prioritized findings and remediation suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference repository configuration, environment examples, CI/CD files, deployment manifests, API schemas, and documentation when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
