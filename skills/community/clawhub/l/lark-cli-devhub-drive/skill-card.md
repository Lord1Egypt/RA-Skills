## Description: <br>
Use when managing Feishu/Lark Drive files through lark-cli or feishu-cli for Dev Hub search, inspect, upload, download, import, export, sync, comments, permissions, and artifact registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to manage Feishu/Lark Drive files through lark-cli or feishu-cli during Dev Hub workflows. It supports Drive discovery, inspection, import, export, sync, comments, permissions guidance, and artifact registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drive commands can read or change files, comments, permissions, exports, uploads, sync targets, and artifact records through the authenticated Lark/Feishu account. <br>
Mitigation: Review each command before execution, especially export, upload, sync, permissions, and artifact writeback operations. <br>
Risk: Downloaded private files may be stored locally if the user asks for export or sync workflows. <br>
Mitigation: Do not store downloaded private files in the repository unless the user explicitly requests it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afengzi/lark-cli-devhub-drive) <br>
- [Publisher profile](https://clawhub.ai/user/afengzi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-run lark-cli or feishu-cli session authenticated to the user's Lark/Feishu account.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
