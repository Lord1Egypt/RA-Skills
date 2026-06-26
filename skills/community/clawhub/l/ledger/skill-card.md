## Description: <br>
Calculate ledger financial metrics and business data. Use when tracking expenses, analyzing investments, or generating financial reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and finance-minded users can use Ledger to keep a simple local file-based ledger, add, list, search, and remove entries, view status and statistics, and export records for reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ledger entries and exports can contain sensitive financial or business records stored on local disk. <br>
Mitigation: Protect ~/.ledger or set LEDGER_DIR to a controlled location, and review exported files before sharing. <br>
Risk: The remove command deletes the selected entry immediately. <br>
Mitigation: List entries and confirm the target line number before removal; keep backups for records that must be retained. <br>


## Reference(s): <br>
- [Ledger on ClawHub](https://clawhub.ai/bytesagain3/ledger) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [BytesAgain publisher profile](https://clawhub.ai/user/bytesagain3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; CLI outputs are plain text, JSONL, or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local ledger data under LEDGER_DIR or ~/.ledger and can export records to JSONL or CSV.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
