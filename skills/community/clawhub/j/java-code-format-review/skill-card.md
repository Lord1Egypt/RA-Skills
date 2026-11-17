## Description:

Use when reviewing AI-generated code for formatting consistency. Enforces naming, structure, comments, and style conventions. Optimized for Java.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyliu1](https://clawhub.ai/user/joeyliu1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill after AI-generated Java code changes to check formatting, naming, comments, exception handling, logging, and related style conventions before commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run repository build tools or formatter commands, including Maven, Gradle, Spotless, and google-java-format, before the target project has been reviewed.

Mitigation: Run automated checks and auto-fix commands only in an isolated environment after reviewing the project, and require separate confirmation before applying fixes.

Risk: Broad style guidance may produce recommendations that conflict with a repository's established formatting or static-analysis configuration.

Mitigation: Use the repository's existing formatter and static-analysis configuration as the baseline, and treat the skill's default Java conventions as fallback guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyliu1/skills/java-code-format-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review report with issue severities, file locations, suggested fixes, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The review report groups findings by P0, P1, and P2 severity and may include counts of detected issues.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
