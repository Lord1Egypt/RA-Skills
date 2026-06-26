## Description: <br>
Personal protective equipment tracker. Use when json ppe tasks, csv ppe tasks, checking ppe status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, safety coordinators, and operations teams use this skill to track PPE inventory records from local shell commands, including status, add, list, search, remove, export, stats, and configuration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remove actions can delete local PPE inventory entries. <br>
Mitigation: Review remove commands and target line numbers before execution. <br>
Risk: Exported PPE records may contain sensitive workplace data and are written to local JSON or CSV files. <br>
Mitigation: Confirm the export location and avoid shared or synced folders unless that storage is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/ppe) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain terminal text with JSONL and CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores PPE records locally under PPE_DIR or ~/.ppe and can export records to ppe-export.json or ppe-export.csv.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
