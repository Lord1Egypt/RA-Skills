## Description: <br>
Reviews Java Maven projects delivered as a ZIP archive or GitLab repository URL for coding standards, naming, module boundaries, maintainability issues, duplicated logic, structure issues, and remediation recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrliugangqiang](https://clawhub.ai/user/mrliugangqiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run a first-pass review of Java Maven projects and produce a formal Markdown coding-standards report with file-level evidence, impact notes, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the Java/Maven project supplied by the user and may include file paths or keyword evidence from source and configuration files in generated reports. <br>
Mitigation: Run it only on projects the agent is allowed to inspect, and review generated reports before sharing them outside the intended audience. <br>
Risk: The bundled scan is a heuristic first-pass review and may miss design, naming, duplication, maintainability, or module-boundary issues. <br>
Mitigation: Treat the report as review support, not final assurance, and pair it with human code review or project-specific checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrliugangqiang/java-maven-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown report, with optional JSON scan results from the bundled scanner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the report under business/ and may include file paths, keyword evidence, impact notes, and remediation advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
