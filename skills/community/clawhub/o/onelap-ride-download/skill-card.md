## Description: <br>
Downloads cycling activity FIT files from Onelap for bulk export of a user's ride data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CKboss](https://clawhub.ai/user/CKboss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to back up Onelap cycling records, export date ranges of ride FIT files, and prepare those files for import into third-party fitness or analysis tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's logged-in Onelap browser session to locate downloadable ride files. <br>
Mitigation: Confirm that the agent should access the logged-in session before running the workflow. <br>
Risk: FIT files can contain private activity, location, and training data. <br>
Mitigation: Review exported files before sharing them and delete local copies when they are no longer needed. <br>
Risk: Download URLs can include time-limited tokens. <br>
Mitigation: Do not publish tokenized links or logs containing those links. <br>
Risk: An incorrect date range or destination path could download or place files somewhere unintended. <br>
Mitigation: Confirm the requested date range and output directory before executing download commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CKboss/onelap-ride-download) <br>
- [Onelap analysis page](https://u.onelap.cn/analysis) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown with inline browser and bash commands, file paths, and download summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the workflow saves FIT activity files to a local date-range directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
