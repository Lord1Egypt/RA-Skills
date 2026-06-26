## Description: <br>
Provides developers with Mobile Meeting / Cloud Video API integration guidance and helper scripts for authentication, meeting management, meeting control, and recording workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thursda](https://clawhub.ai/user/thursda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill to answer Mobile Meeting / Cloud Video API questions, generate request examples, and run helper scripts for token, meeting, and recording workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with sensitive App IDs, App Keys, access tokens, refresh tokens, meeting links, and recording download tokens. <br>
Mitigation: Use test accounts first, replace all sample credentials with placeholders, avoid entering production keys into shared browsers, and keep generated tokens out of logs and chat transcripts. <br>
Risk: Some reference examples use disabled TLS verification patterns such as curl -k while demonstrating authenticated meeting API calls. <br>
Mitigation: Do not copy trust-all TLS examples into production; require certificate validation and review transport security before deployment. <br>
Risk: The documented workflows can create, update, cancel, delete, invite participants to, or access recordings for real meetings. <br>
Mitigation: Require explicit user confirmation before performing state-changing or sensitive retrieval actions, especially cancellation, deletion, participant invitation, and recording access. <br>


## Reference(s): <br>
- [Mobile Meeting Developer Center](https://www.125339.com.cn/developerCenter/ReBar/63/222) <br>
- [Full API Documentation Download](https://www.125339.com.cn/developerCenter/ReBar/63/197) <br>
- [App ID Authentication Overview](https://www.125339.com.cn/developerCenter/ReBar/63/191) <br>
- [Create App ID Token](references/CreateAppIdToken.md) <br>
- [Create Meeting](references/CreateMeeting.md) <br>
- [Search Meetings](references/SearchMeetings.md) <br>
- [Cancel Meeting](references/CancelMeeting.md) <br>
- [Show Recording File Download URLs](references/ShowRecordingFileDownloadUrls.md) <br>
- [Delete Recordings](references/DeleteRecordings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API details, code examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable Python script usage guidance and API request or response examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
