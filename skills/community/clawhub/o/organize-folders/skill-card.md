## Description: <br>
Scans, analyzes, plans, and documents folder organization systems for existing folders and new-file intake, including classification rules, directory naming, execution logs, and Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bojahng](https://clawhub.ai/user/bojahng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inventory messy folders, design durable organization rules, generate folder cleanup plans, and produce reviewable reports before approving any file moves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Folder scans can expose file names, paths, sizes, and timestamps from user-selected directories. <br>
Mitigation: Run the skill only on explicit target folders, start with a small folder, and choose a report directory before generating inventories or plans. <br>
Risk: Incorrect or over-broad move plans could reorganize files in ways the user does not intend. <br>
Mitigation: Review the dry-run and validation output first; approve actual execution only when planned moves and high-risk items are clear. <br>


## Reference(s): <br>
- [Folder Workflow](references/workflow.md) <br>
- [Folder Rules](references/folder-rules.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [Taxonomy Patterns](references/taxonomy-patterns.md) <br>
- [Tooling Design](references/tooling-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON inventories and plans, CSV move plans, JSONL logs, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports and logs are written to a dedicated organize_report directory by default; actual file changes require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
