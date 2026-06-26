## Description: <br>
Reports user-described bugs to an Enterprise WeCom smart sheet, filling predefined fields for issue description, status, and assignee. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wearflatshoestowalktheworld](https://clawhub.ai/user/wearflatshoestowalktheworld) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or support staff can use this skill to turn a user's bug report into a tracked Enterprise WeCom smart sheet record. It is appropriate only when the fixed sheet destination and assignee match the intended workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bug report text may be sent to a fixed Enterprise WeCom smart sheet and stored as a persistent record without clear confirmation. <br>
Mitigation: Use the skill only when that destination is intended, require explicit confirmation before sending, and avoid including secrets, customer data, or other sensitive content. <br>
Risk: The webhook destination and assignee are fixed in the artifact behavior. <br>
Mitigation: Replace hard-coded destinations with private configuration or secrets and review the destination before deployment. <br>
Risk: The metadata declares an unexplained npm dependency. <br>
Mitigation: Review, justify, or remove the dependency before installation in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wearflatshoestowalktheworld/global-bug) <br>
- [Publisher profile](https://clawhub.ai/user/wearflatshoestowalktheworld) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status messages with JSON request payloads for the WeCom smart sheet webhook.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the reported issue description as the primary input and fills remaining fields with predefined defaults.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
