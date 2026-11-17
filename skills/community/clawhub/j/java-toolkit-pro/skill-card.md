## Description:

Java 工具箱专业版 helps developers and engineering teams scan Java repositories, govern shared rulesets and exemptions, review JVM/GC settings, and define test, coverage, and performance gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering teams, and automation workflows use this skill to inspect multi-module Java projects, manage versioned rule policies, configure JVM tuning review, and propose build or coverage gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because routing is broader than expected for a Java toolkit that can run commands and write files.

Mitigation: Install it only for Java repository scanning, ruleset management, JVM/GC review, and build or coverage gate tasks.

Risk: Command execution and file writes can affect a workspace when the task is generic reporting, planning, or non-Java analysis.

Mitigation: Require explicit user direction before running commands or writing files, and keep use limited to the Java workflows described by the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/java-toolkit-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, Java, and Gradle configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured status, result, execution log, and error fields when the skill asks for JSON output.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
