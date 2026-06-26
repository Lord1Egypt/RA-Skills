## Description: <br>
Reviews Java diffs or source files and generates structured Markdown or HTML review reports with severity, issue descriptions, and fix suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxweven](https://clawhub.ai/user/wxweven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Java code changes, source files, and optional design documents for style, exception handling, security, performance, design, and resource-management issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated review reports may include sensitive code, diffs, or design details supplied by the user. <br>
Mitigation: Provide only source files, diffs, and documents that are appropriate for analysis in the active assistant environment. <br>
Risk: Generated HTML reports from untrusted inputs may be shared or opened without review. <br>
Mitigation: Review generated HTML before opening it broadly or distributing it outside the intended audience. <br>


## Reference(s): <br>
- [Java code review rules](references/rules.md) <br>
- [Markdown report template](assets/report-template.md) <br>
- [HTML report template](assets/report-template.html) <br>
- [ClawHub skill page](https://clawhub.ai/wxweven/java-code-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown by default, with HTML available when requested; reports include structured findings and Java code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are organized by severity and may include consistency checks when requirements or design documents are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
