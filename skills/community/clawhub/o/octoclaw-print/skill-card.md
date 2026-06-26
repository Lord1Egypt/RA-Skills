## Description: <br>
Control an OctoPrint 3D printer by monitoring status, capturing webcam snapshots, managing prints, analyzing G-code, checking for errors, and optionally sending Telegram updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peterhanily](https://clawhub.ai/user/peterhanily) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who manage OctoPrint-connected 3D printers use this skill to inspect printer state, review files and G-code, capture snapshots, and request print actions from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real 3D printer by starting, pausing, canceling, uploading files, and changing temperatures. <br>
Mitigation: Require explicit human confirmation before any print-control, upload, cancellation, or temperature-changing command. <br>
Risk: OctoPrint API keys and optional Telegram credentials grant access to printer controls or external message delivery. <br>
Mitigation: Keep credentials private, store them only in the local config file, and use the least-privileged OctoPrint account available. <br>
Risk: Telegram status, snapshots, and messages can send printer data to an external chat. <br>
Mitigation: Leave Telegram fields unset unless the user intentionally wants that integration and has verified the destination chat. <br>


## Reference(s): <br>
- [OctoClaw on ClawHub](https://clawhub.ai/peterhanily/octoclaw-print) <br>
- [peterhanily publisher profile](https://clawhub.ai/user/peterhanily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, code] <br>
**Output Format:** [Markdown and terminal output with optional JSON responses and generated local files such as webcam snapshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local config.json containing OctoPrint and optional Telegram credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
