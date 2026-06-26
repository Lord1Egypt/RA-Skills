## Description: <br>
Track leads locally, manage outreach campaigns, and export as CSV for download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3rdbrain](https://clawhub.ai/user/3rdbrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to track outreach leads in a local workspace, log interactions, generate outreach sequences, and export lead data as CSV for download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The clear command can erase all stored leads immediately. <br>
Mitigation: Require explicit user confirmation before running clear, and recommend exporting or backing up important leads first. <br>
Risk: Lead and interaction records may contain sensitive business or contact data stored in the agent workspace. <br>
Mitigation: Treat the JSON and CSV files as sensitive data, limit access to the workspace, and avoid storing unnecessary personal or confidential details. <br>
Risk: CSV exports can expose stored lead data when downloaded or shared. <br>
Mitigation: Share exported CSV files only with intended recipients and remove exports from the workspace when no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/3rdbrain/outreach-crm) <br>
- [Publisher Profile](https://clawhub.ai/user/3rdbrain) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [CLI text output, generated outreach guidance, local JSON lead storage, and CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes lead data to the agent workspace and prints CSV export paths for download.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
