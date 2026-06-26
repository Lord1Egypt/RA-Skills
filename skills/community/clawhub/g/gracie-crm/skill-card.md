## Description: <br>
Manage and track Gracie AI Receptionist sales leads with CLI commands to add, update, log calls, add notes, and view sales pipeline summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayJJimenez](https://clawhub.ai/user/JayJJimenez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales operators and agent users use this skill to maintain a local CRM for Gracie AI Receptionist prospects, including lead entry, call logging, follow-up tracking, and pipeline review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead and contact data is stored in the skill directory in crm.json. <br>
Mitigation: Install only where local CRM data storage is acceptable, restrict filesystem access to the skill directory, and back up crm.json when the data matters. <br>
Risk: The import command reads from a fixed MASTER_LEAD_LIST.md path when present. <br>
Mitigation: Review the configured import path before running import so only intended lead data is loaded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JayJJimenez/gracie-crm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON data updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores lead records in a local crm.json file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
