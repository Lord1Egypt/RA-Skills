## Description: <br>
Metal Price queries qqthj.com for current metal price tables and exports the results to Excel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiang2023](https://clawhub.ai/user/wangxiang2023) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and market analysts use this skill to automate qqthj.com login, navigate to selected metal categories, collect current price table data, and export the results for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact exposes a website login credential. <br>
Mitigation: Do not use the embedded account unless authorized; rotate the exposed password and provide credentials through a secure runtime input or secret store. <br>
Risk: The artifact directs exports to a specific personal Windows desktop folder. <br>
Mitigation: Confirm or choose an appropriate export directory before running the skill, and verify write permissions before saving files. <br>
Risk: Scheduled or repeated runs could repeatedly log in and write files without fresh confirmation. <br>
Mitigation: Avoid scheduled or repeated execution unless the login, destination path, and file-writing behavior are explicitly approved. <br>


## Reference(s): <br>
- [Global Ferroalloy Network](https://www.qqthj.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Excel .xlsx file with procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports selected metal price data for the requested category and date; the artifact documents a fixed Windows export path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
