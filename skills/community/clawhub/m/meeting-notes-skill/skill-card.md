## Description: <br>
会议纪要助手处理会议录音或转写文本，生成结构化纪要、Action Items、TTS 播报稿和会议思维导图，并支持 ASR 与 TTS 流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2813223285](https://clawhub.ai/user/2813223285) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, meeting facilitators, and agents use this skill to turn recorded or transcribed meetings into structured minutes, decisions, action items, voice briefings, and mind maps. It is intended for Chinese and mixed Chinese-English meeting workflows that need ASR/TTS support and file outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting files may be written persistently to local output directories. <br>
Mitigation: Review the configured output path before use and delete generated meeting artifacts according to the user's retention policy. <br>
Risk: The skill can install local dependencies automatically. <br>
Mitigation: Avoid auto-install mode unless package changes have been reviewed and approved for the environment. <br>
Risk: Cloud ASR or TTS providers may receive raw meeting audio or meeting text. <br>
Mitigation: For confidential meetings, require local-only ASR/TTS providers or obtain explicit approval before using cloud providers. <br>


## Reference(s): <br>
- [Meeting Notes Skill on ClawHub](https://clawhub.ai/2813223285/meeting-notes-skill) <br>
- [Meeting Minutes Output Template](references/output-template.md) <br>
- [Meeting Notes Quality Gate Checklist](references/quality-gate-checklist.md) <br>
- [Homebrew](https://brew.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance plus generated TXT, MP3, HTML, SVG, and XMind artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default final deliverables are a structured minutes file, a brief MP3 audio file, and an HTML mind map with a shared meeting-topic timestamp prefix.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
