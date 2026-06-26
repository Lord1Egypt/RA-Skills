## Description: <br>
Guides analysis of Java, Maven, and Spring dependency security risks, including vulnerability scanning, affected-version verification, transitive dependency review, embedded JAR inspection, CVE impact review, and remediation reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiushuizy](https://clawhub.ai/user/qiushuizy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to analyze Java dependency risk, confirm whether specific versions are affected by known vulnerabilities, inspect Maven or Gradle dependency paths, and produce prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Build and scanner commands may inspect project files, download dependency metadata, query public vulnerability APIs, and generate reports that include private dependency names or repository details. <br>
Mitigation: Run the suggested Maven, Gradle, and vulnerability scanning commands only in repositories you trust, and review generated reports before sharing them outside the project team. <br>
Risk: Scanner output can include false positives or incomplete findings when dependency versions, scopes, exclusions, or runtime paths are not fully resolved. <br>
Mitigation: Use lockfiles, dependency trees, affected-version ranges, and official advisories to confirm findings before treating a dependency as vulnerable. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Execution Principles and Environment](references/01-principles.md) <br>
- [Maven Project Analysis](references/02-maven.md) <br>
- [Gradle Project Analysis](references/03-gradle.md) <br>
- [Vulnerability Scanning Tools](references/04-tools.md) <br>
- [Command Examples](references/05-commands.md) <br>
- [Output and Remediation Templates](references/06-output.md) <br>
- [Reference and FAQ](references/07-reference.md) <br>
- [Maven Dependency Mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html) <br>
- [Gradle Viewing Dependencies](https://docs.gradle.org/current/userguide/viewing_debugging_dependencies.html) <br>
- [CVE](https://www.cve.org/) <br>
- [Spring Security Advisories](https://spring.io/security) <br>
- [OSV API Documentation](https://osv.dev/docs/) <br>
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include vulnerability summaries, dependency evidence, remediation priorities, and uncertainty labels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
