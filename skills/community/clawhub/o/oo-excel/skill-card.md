## Description: <br>
Excel (microsoft.com). Use this skill for ANY Excel request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect, read, create, update, sort, filter, and delete Microsoft Excel workbook data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or remove workbook data through an OOMOL-connected Excel account. <br>
Mitigation: Review each proposed write or destructive payload, confirm the target workbook, worksheet, range, table, and effect, and require explicit user approval before execution. <br>
Risk: Excel workbooks may contain financial, business, or personal data. <br>
Mitigation: Limit actions to the user-approved workbook data needed for the task and inspect returned data before sharing or reusing it. <br>
Risk: First-time setup may require installing the OOMOL CLI. <br>
Mitigation: Review the OOMOL CLI installer before running it when the CLI is not already installed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-excel) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Microsoft Excel](https://www.microsoft.com/microsoft-365/excel) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution; write and destructive operations require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
