## Description:

Java Coding Quality helps agents run a tool-based quality and security gate for Java and Spring Boot code using PMD 7, SpotBugs, and FindSecBugs, then prioritize fixes until Blocker and Critical findings are cleared.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baixuanzhu](https://clawhub.ai/user/baixuanzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill after Java or Spring Boot code changes, before delivery, or during code review to compile, scan, triage, and fix quality and security issues. It is intended for Maven or Gradle JVM projects and falls back to manual checklist review when build tools are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Java build and static-analysis commands and may download Maven or Gradle analysis plugins.

Mitigation: Review proposed commands before execution and run them only in the intended project workspace with the expected build environment.

Risk: The skill can create a .qualitygate directory, update .gitignore, and optionally persist PMD or SpotBugs configuration into project build files.

Mitigation: Use the default zero-intrusion workflow for scanning and approve build-file persistence only when the quality gate should become part of the project or CI process.

Risk: False-positive suppressions could hide real security or quality issues.

Mitigation: Require user confirmation and an explicit justification for suppressions, and do not suppress FindSecBugs security findings automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baixuanzhu/skills/java-coding-quality)
- [Setup and environment](artifact/references/01-setup.md)
- [PMD 7 ruleset](artifact/references/02-pmd-rules.md)
- [SpotBugs and FindSecBugs security scanning](artifact/references/03-spotbugs-security.md)
- [Gate severity and fix workflow](artifact/references/04-fix-workflow.md)
- [Built-in PMD 7 ruleset](artifact/assets/pmd7-ruleset.xml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Java code changes, XML configuration, and scan-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local .qualitygate directory, append .qualitygate/ to .gitignore, and propose optional PMD or SpotBugs persistence only after user approval.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact frontmatter states 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
