## Description: <br>
InvoiceTW helps agents check, record, list, and summarize Taiwan uniform invoice receipts and prize status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ofather](https://clawhub.ai/user/ofather) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use InvoiceTW to manage Taiwan uniform invoice numbers, local receipt records, prize checks, winner lists, and summary statistics. <br>

### Deployment Geography for Use: <br>
Taiwan <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents hard-coded demo invoice-prize results as real Taiwan invoice checks. <br>
Mitigation: Treat prize-checking output as demo guidance only unless the skill is changed to use an official Taiwan Ministry of Finance source. <br>
Risk: Entered receipt details are stored locally in plain JSON files. <br>
Mitigation: Avoid entering sensitive receipt information and protect or remove the local workspace files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ofather/invoicetw) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ofather) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Terminal text with JSON-backed local receipt, win, and report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and writes local receipt tracking data under the user's home workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
