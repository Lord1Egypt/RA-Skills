## Description: <br>
Analyzes PRDs with a Spec Coding workflow to identify backend, frontend, customer-visible, test, and risk impacts before implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohalo](https://clawhub.ai/user/ohalo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, product teams, and reviewers use this skill to convert PRDs into structured impact specifications that can be reviewed before code changes are made. It is aimed at large project impact assessment, cross-team requirement handoff, code-review preparation, test coverage planning, and technical-debt analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect PRDs and relevant repository files during impact analysis. <br>
Mitigation: Limit access to the PRD and repository areas needed for the task, and avoid granting access to secrets or unrelated private repositories. <br>
Risk: Generated impact specifications or optional code-generation outputs may be incomplete or incorrect. <br>
Mitigation: Review the generated specs before implementation and keep any code-generation step under explicit user control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ohalo/prd-impact-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown and JSON change specifications with pseudocode, risk notes, and implementation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect specified PRDs and relevant repository files; optional code generation should remain under explicit user control.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
