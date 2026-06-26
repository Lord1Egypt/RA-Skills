## Description: <br>
This skill guides agents to use the PortEden CLI for permission-based Google Sheets data operations and file management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the PortEden CLI for Google Sheets workflows, including reading and writing ranges, appending rows, exporting links, managing permissions, renaming files, and moving sheets to trash. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using this skill requires trusting PortEden with access to the connected Google account and sheets. <br>
Mitigation: Review token scopes before login and connect only the Google account and sheets intended for PortEden access. <br>
Risk: Write, share, rename, and delete commands can change spreadsheet data or access. <br>
Mitigation: Confirm target file IDs, ranges, and permission changes before running mutating commands; avoid public sharing unless intended. <br>
Risk: Stored credentials or PE_API_KEY can grant access to connected Sheets. <br>
Mitigation: Use the system keyring or protected environment variables and avoid exposing tokens in shared logs or shell history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/porteden/porteden-sheets) <br>
- [PortEden Homepage](https://porteden.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends compact JSON output with the PortEden -jc flag when reading or inspecting sheets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
