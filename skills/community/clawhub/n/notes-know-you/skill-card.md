## Description: <br>
Sync Evernote notebooks to local Markdown, analyze your notes, and update USER.md and memory files so the AI assistant has structured context about the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hxiaom](https://clawhub.ai/user/hxiaom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to sync Evernote or Yinxiang notebooks, convert them into Markdown, analyze personal note content, and update USER.md plus memory files with structured profile, project, and preference insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private Evernote or Yinxiang notes may contain sensitive personal data that the skill analyzes and persists into USER.md and memory files. <br>
Mitigation: Review generated Markdown, USER.md, and memory files before relying on them, and remove sensitive details that should not become lasting AI context. <br>
Risk: Developer tokens or notebook paths can be exposed if stored in shared shell profiles, logs, or command history. <br>
Mitigation: Keep tokens out of shared profiles and history, prefer temporary or secured environment configuration, and rotate tokens if exposure is suspected. <br>
Risk: Scheduled sync can repeatedly process and refresh personal note-derived memory without close review. <br>
Mitigation: Enable scheduled sync only after confirming how to inspect, pause, or disable the schedule and reviewing the first generated outputs. <br>
Risk: AI analysis may be local or remote depending on the agent environment, which affects where note text is processed. <br>
Mitigation: Clarify the active AI backend before analyzing notes and avoid processing notebooks that should not leave the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hxiaom/notes-know-you) <br>
- [Setup guide](references/setup.md) <br>
- [Pandoc installation guide](https://pandoc.org/installing.html) <br>
- [Yinxiang developer token page](https://app.yinxiang.com/api/DeveloperToken.action) <br>
- [Evernote developer token page](https://www.evernote.com/api/DeveloperToken.action) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and concise text status summaries with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update USER.md, MEMORY.md, individual memory files, ENEX exports, and Markdown notebook files from local Evernote or Yinxiang data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
