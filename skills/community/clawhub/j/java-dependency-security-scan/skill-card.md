## Description:

Helps agents analyze dependency security risks in Java, Maven, Gradle, and Spring ecosystem projects, including vulnerability matching, transitive dependency review, embedded JAR inspection, and remediation reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiushuizy](https://clawhub.ai/user/qiushuizy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to investigate Java dependency vulnerabilities, confirm affected versions against dependency evidence, and prepare prioritized remediation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run Maven or Gradle commands that may execute project-controlled build logic.

Mitigation: Ask before executing build-tool or scanner commands, inspect static files and lockfiles first, and use a disposable environment without unrelated secrets or broad filesystem access for untrusted repositories.

Risk: Scanner output or declared dependency versions can produce misleading vulnerability conclusions when effective runtime versions are not confirmed.

Mitigation: Treat scanner results as leads, verify effective versions with dependency trees or lockfiles, and cross-check affected ranges against authoritative advisories before reporting confirmed findings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qiushuizy/skills/java-dependency-security-scan)
- [Execution Principles and Environment](references/01-principles.md)
- [Maven Project Analysis](references/02-maven.md)
- [Gradle Project Analysis](references/03-gradle.md)
- [Vulnerability Scanning Tools](references/04-tools.md)
- [Command Examples](references/05-commands.md)
- [Output and Remediation Templates](references/06-output.md)
- [Reference and FAQ](references/07-reference.md)
- [Maven Dependency Mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
- [Gradle Viewing Dependencies](https://docs.gradle.org/current/userguide/viewing_debugging_dependencies.html)
- [CVE Database](https://www.cve.org/)
- [Spring Security Advisories](https://spring.io/security)
- [OSV Documentation](https://osv.dev/docs/)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with dependency findings, remediation guidance, shell commands, and optional Maven or Gradle snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes evidence-backed vulnerability status, uncertainty labels, runtime relevance, and prioritized fixes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
