## Description: <br>
Render compact generic data tables to PNG images with json-render-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorphwer](https://clawhub.ai/user/sorphwer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn arbitrary structured rows and columns into compact table screenshots with deterministic layout controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run local shell commands and install npm or Playwright dependencies when required. <br>
Mitigation: Install and run it only in environments where local command execution and dependency installation are acceptable. <br>
Risk: Optional sub-agent or alternate-model routing can expose table data to another execution path. <br>
Mitigation: Keep sensitive table rendering in the main agent unless the output handoff and data flow are explicitly acceptable. <br>


## Reference(s): <br>
- [Compact Table Spec Template](references/compact-table-spec.template.json) <br>
- [Compact Generic Table Template](references/compact-table-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sorphwer/json-render-table) <br>
- [Publisher Profile](https://clawhub.ai/user/sorphwer) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and PNG file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Usually writes PNG output to a local path; Base64 output is used only when explicitly requested.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
