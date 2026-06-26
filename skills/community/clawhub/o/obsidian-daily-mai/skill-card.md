## Description: <br>
Create and manage Obsidian daily notes for daily logs, work summaries, session activity records, and follow-up action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jini92](https://clawhub.ai/user/jini92) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn session context and daily work activity into structured Obsidian daily notes with completed work, next actions, and vault-aware filenames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily notes can persist sensitive session or work details into an Obsidian vault, including vaults synced to cloud services. <br>
Mitigation: Review generated filenames and note content before saving, and avoid recording sensitive details in synced vaults unless that storage is approved. <br>
Risk: Misconfigured daily-note paths can place generated Markdown in the wrong vault folder. <br>
Mitigation: Configure the daily-note folder explicitly and confirm the target path before writing the note. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jini92/obsidian-daily-mai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown daily-note content with filename guidance and optional UTF-8 file-writing commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local vault paths and daily work details supplied by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
