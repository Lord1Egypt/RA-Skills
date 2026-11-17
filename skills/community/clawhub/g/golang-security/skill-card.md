## Description:

Golang Security guides agents through Go security review, auditing, and secure coding across injection, cryptography, filesystem, network, cookie, secrets, memory-safety, logging, and tooling concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review pull requests, audit Go codebases, and implement security-sensitive Go changes with vulnerability-domain guidance and scanner-backed verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and edit Go code and propose security fixes that may be incomplete or incorrect.

Mitigation: Review generated changes before applying them, keep fixes focused, and run relevant Go tests plus security scanners before deployment.

Risk: The documented tool install uses mutable latest versions for govulncheck and references additional scanner tooling.

Mitigation: Pin scanner versions or use an internal module mirror in stricter environments.

Risk: Large audits may use multiple agents and produce overlapping or noisy findings.

Mitigation: Deduplicate findings, rank by severity, and validate each issue against data flow and trust-boundary evidence before remediation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-security)
- [cc-skills-golang homepage](https://github.com/samber/cc-skills-golang)
- [Security Architecture Patterns](references/architecture.md)
- [Security Review Checklist](references/checklist.md)
- [Cookie Security Rules](references/cookies.md)
- [Cryptography Security Rules](references/cryptography.md)
- [Filesystem Security Rules](references/filesystem.md)
- [Injection Security Rules](references/injection.md)
- [Logging Security Rules](references/logging.md)
- [Memory Safety Security Rules](references/memory-safety.md)
- [Network/Web Security Rules](references/network.md)
- [Secrets Management Security Rules](references/secrets.md)
- [Third-Party Data Leak Rules](references/third-party.md)
- [Threat Modeling Guide](references/threat-modeling.md)
- [Go Security Best Practices](https://go.dev/doc/security/best-practices)
- [gosec Security Linter](https://github.com/securego/gosec)
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [OWASP Go Secure Coding Practices](https://owasp.org/www-project-go-secure-coding-practices-guide/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, review findings, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Go file edits, scanner commands, dependency checks, and multi-agent audit summaries depending on the user's task.]

## Skill Version(s):

1.2.0 (source: evidence release, artifact metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
