## Description:

Unified security scanner that catches leaked secrets, credentials, and code vulnerabilities before they reach your remote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celstnblacc](https://clawhub.ai/user/celstnblacc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan git repositories for leaked credentials, vulnerable code patterns, and security findings before commits, reviews, or CI releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags this release as suspicious because it advises overriding an installation warning.

Mitigation: Review the skill before installing and avoid using --force unless the exact artifact has been independently verified.

Risk: The skill relies on externally installed scanner tools whose versions are not pinned by the release evidence.

Mitigation: Use pinned, verified versions of gitleaks and shipguard and document the versions used in CI or pre-commit environments.

Risk: Repository scans and generated reports may expose secrets to installed scanner tools or report storage.

Mitigation: Run scans in trusted environments, restrict report access, and rotate any credentials reported as exposed.

## Reference(s):

- [Git Security Scanner on ClawHub](https://clawhub.ai/celstnblacc/skills/git-security-scanner)
- [Publisher profile](https://clawhub.ai/user/celstnblacc)
- [Clawdis homepage](https://github.com/celstnblacc)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [gitleaks releases](https://github.com/gitleaks/gitleaks/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON, SARIF, markdown, or terminal scan reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide pre-commit hook setup, scanner configuration, targeted scans, full history audits, and remediation steps.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
