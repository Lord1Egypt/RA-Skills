## Description: <br>
Personal relationship manager powered by Feishu/Lark Bitable for tracking contacts, interactions, birthdays, anniversaries, and proactive reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndreLYL](https://clawhub.ai/user/AndreLYL) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals and personal users use this skill with OpenClaw and Feishu/Lark Bitable to remember relationship details, log interactions, import contacts, and receive birthday, anniversary, and relationship maintenance reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically save casual relationship details into Feishu/Lark with limited per-action confirmation. <br>
Mitigation: Use a dedicated Bitable, review saved entries regularly, and ask the agent to confirm sensitive or ambiguous updates before storing them. <br>
Risk: Bulk contact import and phone contact synchronization can upload more personal data than intended. <br>
Mitigation: Run dry-run previews first, import only files you have reviewed, and avoid ADB phone sync unless you have confirmed exactly what will be uploaded. <br>
Risk: Feishu/Lark credentials and Bitable access can expose relationship and contact data if over-permissioned. <br>
Mitigation: Use a least-privilege Feishu app, keep credentials in the configured OpenClaw file or environment only, and rotate credentials if they may have been shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AndreLYL/person-crm) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Feishu](https://www.feishu.cn) <br>
- [Lark](https://www.larksuite.com) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu/Lark Bitable configuration and may parse CSV or vCard contact files before saving records.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
