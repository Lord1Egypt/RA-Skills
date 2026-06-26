## Description: <br>
Auto meeting notes and action item execution loop for transcripts, recordings, summaries, action items, and follow-up workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DTTNpole-commits](https://clawhub.ai/user/DTTNpole-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn meeting recordings or transcripts into notes, decisions, and action items, with optional delivery to workplace tools such as Feishu, WeCom, and Notion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts, summaries, action items, and user identifiers may be sent to configured external services. <br>
Mitigation: Enable only the integrations needed, use local transcription mode when appropriate, and confirm destinations before posting or creating records. <br>
Risk: Broad trigger wording could cause the skill to run or post meeting content in more situations than intended. <br>
Mitigation: Narrow invocation triggers and require explicit user confirmation before sending messages, creating tasks, or charging usage. <br>
Risk: Webhook or download URLs could send data to unintended hosts if not reviewed. <br>
Mitigation: Validate webhook and recording-download hosts against approved workplace domains before use. <br>
Risk: Cleanup behavior can delete local recordings passed into the workflow. <br>
Mitigation: Limit cleanup to temporary downloaded or extracted files and avoid deleting original user-provided recordings. <br>
Risk: Packaging and entry-point issues may prevent expected installation or execution. <br>
Mitigation: Add the missing requirements file, verify imports and entry points, and test the core processor before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DTTNpole-commits/meetingos) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [Feishu Open Platform API](https://open.feishu.cn/open-apis) <br>
- [WeCom API](https://qyapi.weixin.qq.com/cgi-bin) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, text summaries, action-item lists, Python helper scripts, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process local audio or video files, optionally call configured external services, and may create or post meeting records when credentials are provided.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
