## Description: <br>
Golang Security helps agents write, review, and audit Go code for vulnerabilities across injection, cryptography, filesystem, network, cookie, secrets, memory-safety, logging, and security-tooling concerns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide Go security reviews, audits, and fixes across common vulnerability classes, with supporting checklists, examples, and tool commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence ordinary Go coding tasks and includes broad read, edit, Go tooling, git, web lookup, and sub-agent behaviors during reviews or audits. <br>
Mitigation: Use it in trusted workspaces, review proposed edits and commands before execution, and keep audit scope clear before launching broad scans. <br>
Risk: Some examples are imperfect and may be unsafe if copied without adaptation. <br>
Mitigation: Treat examples as review guidance, validate them against project requirements, and run normal Go tests and security tooling before accepting changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-security) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/samber) <br>
- [OpenClaw Homepage](https://github.com/samber/cc-skills-golang) <br>
- [Go Security Best Practices](https://go.dev/doc/security/best-practices) <br>
- [gosec Security Linter](https://github.com/securego/gosec) <br>
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck) <br>
- [OWASP Go Secure Coding Practices](https://owasp.org/www-project-go-secure-coding-practices-guide/) <br>
- [Security Architecture Patterns](references/architecture.md) <br>
- [Security Review Checklist](references/checklist.md) <br>
- [Cookie Security Rules](references/cookies.md) <br>
- [Cryptography Security Rules](references/cryptography.md) <br>
- [Filesystem Security Rules](references/filesystem.md) <br>
- [Injection Security Rules](references/injection.md) <br>
- [Logging Security Rules](references/logging.md) <br>
- [Memory Safety Security Rules](references/memory-safety.md) <br>
- [Network/Web Security Rules](references/network.md) <br>
- [Secrets Management Security Rules](references/secrets.md) <br>
- [Third-Party Data Leak Rules](references/third-party.md) <br>
- [Threat Modeling Guide](references/threat-modeling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Go code examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity ratings, DREAD scoring, checklists, remediation guidance, and Go security-tool commands.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
