## Description:

Generates GitHub Actions workflow files for CI/CD, tests, deployment, Docker publishing, releases, Dependabot updates, and scheduled jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to generate starter GitHub Actions workflows for common repository automation tasks such as CI, deployment, Docker publishing, release publishing, dependency updates, and scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes or overwrites GitHub Actions workflow files in the current repository.

Mitigation: Review the generated YAML before committing it, especially action versions, workflow permissions, secrets exposure, and deployment behavior.

Risk: Generated automation may not match a repository's build, test, deployment, or secret-handling requirements.

Mitigation: Treat generated workflows as a starting point and adapt them to the repository before enabling them on protected branches.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunshine-del-ux/skills/github-actions-generator)

## Skill Output:

**Output Type(s):** [configuration, code, shell commands]

**Output Format:** [GitHub Actions YAML workflow files and brief terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes workflow files under .github/workflows in the current repository.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
