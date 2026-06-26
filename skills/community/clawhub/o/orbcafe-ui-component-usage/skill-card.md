## Description: <br>
Route ORBCAFE UI requests to the correct module skill and enforce official examples-based integration baseline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SHENRUIYANG](https://clawhub.ai/user/SHENRUIYANG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to classify ORBCAFE UI integration requests, choose the correct module skill, and produce minimal runnable guidance using public ORBCAFE UI APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose npm install, build, or startup commands for ORBCAFE UI integration. <br>
Mitigation: Review package names and versions, and run commands only in the intended project. <br>
Risk: The skill routes to companion ORBCAFE module skills whose behavior is outside this router's direct evidence. <br>
Mitigation: Review companion module skills before using generated implementation guidance. <br>


## Reference(s): <br>
- [ORBCAFE UI component usage release page](https://clawhub.ai/SHENRUIYANG/orbcafe-ui-component-usage) <br>
- [Skill routing map](references/skill-routing-map.md) <br>
- [Module contracts](references/module-contracts.md) <br>
- [Module contracts JSON](references/module-contracts.json) <br>
- [Integration baseline](references/integration-baseline.md) <br>
- [Public export index](references/public-export-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and bash blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include a module decision, paste-ready code, data shape, verification steps, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
