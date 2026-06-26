## Description: <br>
当用户想保存文章或链接到笔记库、搜索已保存文章、或配置 NoteHelper API 密钥时触发，并指导代理使用 /notehelper save、link、search 和 config 命令。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notesynchelper](https://clawhub.ai/user/notesynchelper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to save article content or bare URLs into a NoteHelper-backed note library, search saved articles, and configure the API key needed to reach the external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided notes, URLs, article content, and search terms may be sent to the external NoteHelper service, including bare URLs when the link route is selected. <br>
Mitigation: Install only if you trust notebooksyncer.com, prefer explicit /notehelper link or /notehelper save commands, and confirm ambiguous bare URLs before sending them. <br>
Risk: The API key is stored locally and used as a request header, so exposure could allow use of the note service. <br>
Mitigation: Store the key only in ~/.openclaw/notehelper.json or NOTEHELPER_API_KEY, avoid sharing command transcripts that contain it, and revoke the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/notesynchelper/notehelper) <br>
- [NoteHelper homepage](https://notebooksyncer.com) <br>
- [OpenClaw NoteHelper service](https://claw.notebooksyncer.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell, JSON, curl, and GraphQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTEHELPER_API_KEY for save, link, and search actions; may send user-provided article content, URLs, and search terms to claw.notebooksyncer.com.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
