## Description: <br>
Reviews AI-generated Java code for formatting consistency, naming, structure, comments, and style conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyliu1](https://clawhub.ai/user/joeyliu1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review AI-generated or modified Java code before committing, focusing on readability, consistency, maintainability, and Alibaba Java Development Manual style conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broaden a formatting review into general Java code-quality review. <br>
Mitigation: Keep use focused on style, naming, structure, comments, and maintainability unless the user explicitly requests broader review. <br>
Risk: Suggested Maven, Gradle, static-analysis, or auto-format commands may execute project build scripts or rewrite Java files. <br>
Mitigation: Require explicit approval before running build, scanner, or auto-format commands, and use the skill only in repositories the user trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joeyliu1/skills/java-code-format-review) <br>
- [Publisher profile](https://clawhub.ai/user/joeyliu1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with optional shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity-ranked findings, file and line references, statistics, and optional formatter commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
