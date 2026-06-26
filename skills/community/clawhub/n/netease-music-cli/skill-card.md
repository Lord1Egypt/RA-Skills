## Description: <br>
Uses ncm-cli to operate NetEase Cloud Music for playback, song search, playback controls, queue management, status checks, and playlist playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JunfengL](https://clawhub.ai/user/JunfengL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent translate music playback, search, playlist, queue, login, and configuration requests into safe ncm-cli workflows for NetEase Cloud Music. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can pass summaries of recent conversation context to ncm-cli, which may expose unrelated sensitive information. <br>
Mitigation: Use the skill only in task-focused chats, avoid unrelated sensitive content in the session, and review command arguments before execution when sensitive context may be present. <br>
Risk: The skill depends on the local ncm-cli setup and NetEase credentials or appId/privateKey values. <br>
Mitigation: Install ncm-cli from a trusted source, protect login sessions and API keys, and avoid sharing credential values in chat. <br>


## Reference(s): <br>
- [NetEase Cloud Music Open Platform API Key Documentation](https://developer.music.163.com/st/developer/document?docId=9504d35aa41a47c6ac9830b2dbf48f94) <br>
- [ClawHub Skill Page](https://clawhub.ai/JunfengL/netease-music-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include NetEase Cloud Music resource links and ncm-cli command examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
