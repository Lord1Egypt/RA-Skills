## Description: <br>
Build ORBCAFE standard report/list pages with CStandardPage, CTable, CSmartFilter, useStandardReport, persistence, and quickCreate/quickEdit/quickDelete using official examples-proven patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SHENRUIYANG](https://clawhub.ai/user/SHENRUIYANG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to implement ORBCAFE report and list pages with the correct component pattern, persistence identity, pagination behavior, i18n setup, and quick operation callbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup commands may change npm dependencies in the consuming project. <br>
Mitigation: Install only in the intended ORBCAFE UI project and review dependency changes before running setup. <br>
Risk: Generated quick create, edit, or delete callbacks could bypass application controls if copied without adaptation. <br>
Mitigation: Ensure callbacks enforce the application's normal authorization, confirmation, and audit behavior. <br>
Risk: ALL pagination mode can send limit=-1 to a backend that does not support it. <br>
Mitigation: Map unsupported ALL pagination explicitly in fetchData before calling the backend. <br>


## Reference(s): <br>
- [StdReport Component Selection](references/component-selection.md) <br>
- [StdReport Guardrails](references/guardrails.md) <br>
- [StdReport Recipes](references/recipes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/SHENRUIYANG/orbcafe-stdreport-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript/TSX examples and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mode selection, data contract, verification steps, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
