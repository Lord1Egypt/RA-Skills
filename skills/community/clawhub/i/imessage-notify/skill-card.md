## Description: <br>
Send iMessage notifications to an iPhone from a Mac's Messages app, including text, images, videos, audio, files, and URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankxia2013](https://clawhub.ai/user/frankxia2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent send iMessage alerts from Mac-based automated tasks, including task completion notices, screenshots, reports, files, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts default to a specific hardcoded Apple ID recipient. <br>
Mitigation: Install only when that recipient is intentionally yours, or change the scripts to require a local user-configured recipient before use. <br>
Risk: Automated use can transmit text, screenshots, reports, files, and URLs without a safety gate. <br>
Mitigation: Avoid routing secrets or private files through this skill; add explicit confirmation before sending sensitive task outputs. <br>
Risk: Message and attachment values are passed into AppleScript-driven sends. <br>
Mitigation: Review inputs before execution and add proper AppleScript escaping before using untrusted content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/frankxia2013/imessage-notify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Mac with Messages signed in to iMessage and a configured recipient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
