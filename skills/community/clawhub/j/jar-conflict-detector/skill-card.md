## Description:

Detects JAR dependency conflicts, version inconsistencies, duplicate JARs, and known incompatible dependency pairs in Spring Boot Maven or Gradle microservice projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yssnb](https://clawhub.ai/user/yssnb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and build/release engineers use this skill to scan Spring Boot Maven or Gradle projects for dependency conflicts before upgrades, troubleshooting, or CI/CD deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run Maven or Gradle project build logic, including repository-provided Gradle wrappers.

Mitigation: Run it only on trusted projects, or execute it in a disposable sandbox or container with no secrets, limited filesystem access, and controlled network access.

Risk: Live dependency analysis against untrusted Maven or Gradle repositories can execute or retrieve project-controlled build behavior.

Mitigation: Disable or isolate live build execution when analyzing untrusted repositories; prefer static parsing when isolation is not available.

Risk: Generated HTML reports may contain project-derived content.

Mitigation: Treat generated HTML reports as untrusted content and review them in an isolated browser context.

## Reference(s):

- [JAR conflict patterns and remediation guide](references/conflict_patterns.md)
- [ClawHub skill page](https://clawhub.ai/yssnb/skills/jar-conflict-detector)
- [Publisher profile](https://clawhub.ai/user/yssnb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated HTML, TXT, or JSON conflict reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create conflict-report.html, conflict-report.txt, or conflict-report.json depending on the selected report format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
