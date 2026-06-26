## Description: <br>
查询灵犀Note销售录音和会议录音列表，并根据列表返回的数据查看录音详情。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liubf1215](https://clawhub.ai/user/liubf1215) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or teams with authorized Lingxi Note access use this skill to query sales and meeting recording lists, inspect returned recording details, and configure the API key needed for those requests. It should be used only for recordings the user is authorized to access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive Lingxi API key. <br>
Mitigation: Store the key with restrictive permissions, avoid displaying it in terminals or screen shares, and rotate it if exposure is possible. <br>
Risk: Recording responses may include private transcripts, summaries, analytics, and audio URLs. <br>
Mitigation: Use only with authorized Lingxi accounts, avoid shared chats for private recording data, and show only the details needed for the request. <br>
Risk: List queries can retrieve broad recording data by default. <br>
Mitigation: Review returned items before sharing them and use API-provided recording IDs for detail requests instead of inventing identifiers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liubf1215/lingxiai-note-recording) <br>
- [配置灵犀API](references/config.md) <br>
- [录音文件列表查询](references/list.md) <br>
- [Lingxi API base URL](https://aiapi.szyldata.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown responses with optional curl commands and parsed JSON recording data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LYK_API_KEY and may return private transcripts, summaries, analysis fields, and audio URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
