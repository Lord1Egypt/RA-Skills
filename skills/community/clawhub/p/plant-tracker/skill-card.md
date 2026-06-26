## Description: <br>
Personal plant and garden management for gardeners. Track your plants, set care schedules, and monitor growth. Use when you need to manage your garden, track watering/fertilizing schedules, or maintain plant inventories. Security: file exports are restricted to safe directories only (workspace, home, /tmp). Perfect for home gardeners, indoor plant enthusiasts, and anyone growing their own food. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johstracke](https://clawhub.ai/user/johstracke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External gardeners and plant owners use this skill to maintain a local plant inventory, record watering and other care actions, search plant records, and export their collection history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant locations and care notes are stored on disk and included in exports. <br>
Mitigation: Avoid entering sensitive location details or private notes unless local storage and exported Markdown files are acceptable for the intended environment. <br>
Risk: The export command can overwrite a selected local file. <br>
Mitigation: Choose export filenames deliberately and review the destination path before running an export. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [CLI text output, local JSON storage, and Markdown exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores plant records locally under ~/.openclaw/workspace/plants_db.json and can export user-selected Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
