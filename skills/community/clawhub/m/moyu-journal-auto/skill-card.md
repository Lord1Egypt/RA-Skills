## Description: <br>
Records playful local journaling entries about workplace downtime, summarizes daily and weekly activity, and can reframe those notes as a polished work log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SwiftUIs](https://clawhub.ai/user/SwiftUIs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub users can invoke this skill to track downtime notes, generate humorous daily or weekly summaries, and create a work-log version of the same local journal data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive workplace and personal activity logs locally. <br>
Mitigation: Review and delete entries in ~/.openclaw/moyu-journal/ as needed, and avoid recording confidential workplace details. <br>
Risk: Optional browser-history, calendar, or chat-history access can expose more personal context than basic journaling requires. <br>
Mitigation: Keep those optional permissions disabled unless they are explicitly needed for a specific summary. <br>
Risk: Filesystem access is required for the journal workflow and can create durable records. <br>
Mitigation: Enable filesystem access only after accepting local retention, and periodically inspect the storage directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SwiftUIs/moyu-journal-auto) <br>
- [Publisher profile](https://clawhub.ai/user/SwiftUIs) <br>
- [Publisher homepage](https://x.com/walletgonegirl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style conversational responses with local file paths and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON journal files under ~/.openclaw/moyu-journal/ when filesystem access is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
