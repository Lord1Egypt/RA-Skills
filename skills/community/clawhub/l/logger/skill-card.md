## Description: <br>
Appends log entries, audit trails, and automated event records to a pre-configured Google Sheet using PortEden Secure access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to append structured event logs, audit trails, task logs, and error records to a configured Google Sheet through the PortEden CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires credentials that can access Google Drive and Sheets. <br>
Mitigation: Install only when PortEden CLI access is trusted, review token scope, and use a token with the minimum required Drive access. <br>
Risk: Log entries may expose secrets, personal data, regulated records, confidential prompts, or other sensitive information in the destination sheet. <br>
Mitigation: Avoid logging sensitive data unless the sheet has appropriate access controls and retention rules. <br>
Risk: Rows may be appended to the wrong spreadsheet or range if the target sheet is misconfigured. <br>
Mitigation: Set the sheet ID deliberately, read the header row before appending, and verify recent rows after logging. <br>


## Reference(s): <br>
- [PortEden homepage](https://porteden.com) <br>
- [ClawHub skill page](https://clawhub.ai/porteden/logger) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PortEden CLI commands for Google Sheets authentication, sheet discovery, appending rows, and verification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
