## Description: <br>
A Chinese Feishu content-management assistant that helps creators generate hot-list-backed topic ideas, track publishing metrics in Feishu Bitable, manage content calendars, and produce monthly review reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a799549967-lang](https://clawhub.ai/user/a799549967-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators and social-media operators use this skill to connect a Feishu Bitable workspace, generate Chinese topic ideas from trending lists, update publishing metrics by conversation, find stale drafts, and summarize monthly performance patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide sensitive Feishu App ID and App Secret values in chat. <br>
Mitigation: Use a dedicated low-privilege Feishu app and test table, prefer a secure configuration path when available, and rotate any secret already shared in chat. <br>
Risk: The release has a Notion-versus-Feishu identity mismatch that may confuse users about the service being connected. <br>
Mitigation: Install and use it only when the intended target is Feishu, and verify the connected table before allowing record creation or updates. <br>
Risk: Generated topics or metric updates can be written to incorrect Feishu records, especially when fuzzy title matching is involved. <br>
Mitigation: Confirm target records before writes and review generated topics, metrics, and monthly summaries before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/a799549967-lang/notion-content-hub-cn) <br>
- [Publisher profile](https://clawhub.ai/user/a799549967-lang) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [完整使用指南_闭环流程+飞书配置.md](artifact/完整使用指南_闭环流程+飞书配置.md) <br>
- [操作说明.md](artifact/操作说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance, Shell commands] <br>
**Output Format:** [Chinese conversational text and Markdown reports with inline configuration examples and API-backed Feishu updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write records and fields to a user-provided Feishu Bitable after configuration.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
