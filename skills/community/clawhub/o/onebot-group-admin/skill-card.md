## Description: <br>
QQ 群管理操作，通过 OneBot 11 API 实现群名修改、群公告、禁言、踢人、设置管理员、全员禁言等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangalexhy](https://clawhub.ai/user/zhangalexhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and QQ bot operators use this skill to run OneBot 11 group administration actions such as renaming groups, publishing notices, muting or removing members, setting administrators, and retrieving group or member information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad QQ bot administrator powers, including member moderation, administrator changes, message deletion, and public group updates. <br>
Mitigation: Install only for a trusted publisher and intended bot-control use case; restrict the script to approved group-management actions and require explicit confirmation for sensitive actions. <br>
Risk: The script includes an embedded fallback OneBot token. <br>
Mitigation: Remove the fallback token and configure a deployment-specific token through ONEBOT_WS_TOKEN before use. <br>
Risk: The @/path/to/file parameter form can read local file contents into API parameters. <br>
Mitigation: Avoid the @/path/to/file form unless the file content and destination action have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangalexhy/onebot-group-admin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a OneBot WebSocket endpoint and token; sensitive group-management actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
