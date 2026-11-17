## Description:

Design, debug, and harden GitHub Actions workflows with reusable pipelines, safe permissions, and faster CI and release automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design, review, debug, harden, and tune GitHub Actions workflows for CI, release, and deployment automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow edits, live GitHub API actions, release changes, or deployment-affecting operations can alter repository or delivery behavior.

Mitigation: Confirm the intended mutation boundary before those actions and keep deployment credentials in GitHub-managed secrets, environments, or OIDC.

Risk: Local repo-context notes may contain operational details about repositories, protected branches, environments, incidents, and rollback rules.

Mitigation: Store only concise workflow context in ~/github-actions/ and do not persist secrets, copied credentials, or sensitive log dumps.

Risk: Guidance for untrusted pull requests or overly broad workflow permissions could expand CI/CD blast radius if applied without review.

Mitigation: Use explicit minimal permissions, protected environments, short-lived credentials, and reviewer confirmation for privileged or production-facing workflow paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/github-actions)
- [GitHub Actions skill homepage](https://clawic.com/skills/github-actions)
- [GitHub](https://github.com)
- [GitHub REST API](https://api.github.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with YAML and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow file drafts, review findings, triage steps, release guidance, and local setup notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
