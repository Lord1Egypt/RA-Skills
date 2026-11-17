## Description:

Securely clone GitHub projects with comprehensive safety checks, dependency analysis, and security recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tugocoffe](https://clawhub.ai/user/tugocoffe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to clone GitHub repositories, inspect project structure and dependency files, and receive safety-focused installation guidance before running unfamiliar code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The clone script can delete an existing user-supplied target directory after overwrite confirmation.

Mitigation: Use disposable or clearly dedicated target directories, preferably temporary paths, and inspect the resolved target path before approving overwrite.

Risk: The documented --no-check option bypasses repository safety checks.

Mitigation: Keep safety checks enabled for normal use and avoid --no-check unless the repository has already been reviewed through another trusted process.

Risk: Dependency and package mirror commands are recommendations for third-party code and may be unsafe if run without review.

Mitigation: Manually inspect dependency files, package sources, and install commands, then run any installation only in an isolated environment without elevated privileges.

Risk: The server security verdict is suspicious despite the skill's own low-risk metadata.

Mitigation: Treat evidence.security as authoritative, review the security summary and guidance before installation, and do not rely on the bundled validation scripts as proof of security.

## Reference(s):

- [GitHub Security Best Practices](https://docs.github.com/en/security)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [npm Security Audit Guide](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities)
- [Git Shallow Clone Documentation](https://git-scm.com/docs/git-clone#Documentation/git-clone.txt---depthltdepthgt)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and structured security recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub API checks, repository file summaries, dependency previews, and manual installation commands.]

## Skill Version(s):

2.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
