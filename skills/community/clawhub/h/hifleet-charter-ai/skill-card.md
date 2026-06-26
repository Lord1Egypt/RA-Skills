## Description: <br>
HiFleet租船AI helps shipping users manage vessel and cargo email intelligence locally and query HiFleet liner schedules through a cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuwanchu](https://clawhub.ai/user/xuwanchu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Shipping operators and chartering professionals use this skill to search personal mailbox-based vessel and cargo opportunities, structure maritime email information, and query HiFleet liner schedules when an API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal business email may be synced and indexed without clear privacy, deletion, or sync-boundary details. <br>
Mitigation: Use a dedicated mailbox, restricted folder, or app-specific credential, and confirm local memory, SQLite storage, deletion, and sync-stop procedures before production use. <br>
Risk: The skill requires sensitive credentials for mailbox access and HiFleet API access. <br>
Mitigation: Limit credential scope, rotate credentials when access changes, and avoid sharing credentials in prompts or logs. <br>
Risk: Cloud schedule queries may send data to HiFleet's API. <br>
Mitigation: Confirm what request data is sent to the cloud API and avoid submitting confidential chartering details unless approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuwanchu/hifleet-charter-ai) <br>
- [Publisher profile](https://clawhub.ai/user/xuwanchu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require mailbox credentials, local memory or SQLite state, and a HiFleet API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
