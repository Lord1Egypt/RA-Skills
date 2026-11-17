## Description:

Guides agents through Mobile Meeting/Cloud Video API integration for authentication, meeting management, meeting control, recording workflows, and related code examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thursda](https://clawhub.ai/user/thursda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to answer Mobile Meeting API questions, locate the correct endpoint documentation, and generate request examples for authentication, meeting lifecycle, meeting control, attendance, and recording workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live API credentials, access tokens, and meeting data.

Mitigation: Review and adapt the examples before use, run helper scripts only in private terminals, and avoid logging or sharing App Keys, access tokens, meeting IDs, or recording URLs.

Risk: Reference examples include TLS-bypass command patterns such as curl -k.

Mitigation: Use normal certificate validation for API calls and do not copy TLS-bypass examples into production code.

Risk: The bundled browser signing tool accepts App Key input while loading a remote CryptoJS dependency.

Mitigation: Remove or pin the remote dependency before entering real credentials, or use a reviewed local signer.

## Reference(s):

- [Mobile Meeting Developer Center](https://www.125339.com.cn/developerCenter/ReBar/63/222)
- [Mobile Meeting API Documentation Download](https://www.125339.com.cn/developerCenter/ReBar/63/197)
- [App ID Authentication Overview](https://www.125339.com.cn/developerCenter/ReBar/63/191)
- [执行App ID鉴权 - CreateAppIdToken](references/CreateAppIdToken.md)
- [创建会议 - CreateMeeting](references/CreateMeeting.md)
- [查询会议列表 - SearchMeetings](references/SearchMeetings.md)
- [取消预约会议 - CancelMeeting](references/CancelMeeting.md)
- [修改会议 - UpdateMeeting](references/UpdateMeeting.md)
- [开始会议 - StartMeeting](references/StartMeeting.md)
- [查询会议详情 - ShowMeetingDetail](references/ShowMeetingDetail.md)
- [查询历史会议 - SearchHisMeetings](references/SearchHisMeetings.md)
- [查询历史会议详情 - ShowHisMeetingDetail](references/ShowHisMeetingDetail.md)
- [邀请与会者 - InviteParticipant](references/InviteParticipant.md)
- [查询在线与会者 - ListOnlineConfAttendee](references/ListOnlineConfAttendee.md)
- [查询历史会议会控记录 - SearchCtlRecordsOfHisMeeting](references/SearchCtlRecordsOfHisMeeting.md)
- [查询历史会议参会记录 - SearchAttendanceRecordsOfHisMeeting](references/SearchAttendanceRecordsOfHisMeeting.md)
- [查询录制列表 - SearchRecordings](references/SearchRecordings.md)
- [查询录制详情 - ShowRecordingDetail](references/ShowRecordingDetail.md)
- [查询录制文件下载链接 - ShowRecordingFileDownloadUrls](references/ShowRecordingFileDownloadUrls.md)
- [删除录制文件 - DeleteRecordings](references/DeleteRecordings.md)
- [获取会议鉴权随机数 - CreateAuthRandom](references/CreateAuthRandom.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with API request details, parameter tables, code snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include runnable Python helper script usage and Mobile Meeting API parameters drawn from local reference documents.]

## Skill Version(s):

1.0.1 (source: server release; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
