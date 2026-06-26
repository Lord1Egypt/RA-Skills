## Description: <br>
Checks Java code against Alibaba P3C 2022 standards for naming, exception handling, concurrency, database usage, OOP, security, and unit testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohalo](https://clawhub.ai/user/ohalo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review Java files or modules against P3C code-quality rules and produce a categorized Markdown report with findings, severity, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create local Markdown report files in the workspace. <br>
Mitigation: Run it from a workspace where report output is acceptable and confirm the requested business, test, and module names before writing files. <br>
Risk: Static P3C checks and generated recommendations can include false positives or miss context-specific exceptions. <br>
Mitigation: Review the generated report before using it for code review, release gating, or remediation work. <br>


## Reference(s): <br>
- [p3c-code-quality on ClawHub](https://clawhub.ai/ohalo/p3c-code-quality) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes writing timestamped reports under a doc-based test report path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
