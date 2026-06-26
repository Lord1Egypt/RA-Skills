## Description: <br>
Update freznel's Obsidian daily note with timestamped activity entries, especially day recaps, travel logs, itineraries, movement updates, and "I did X at Y time" messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freznel10](https://clawhub.ai/user/freznel10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users can use this skill to turn natural-language day recaps, travel logs, movement updates, meals, errands, and meetings into timestamped entries in an Obsidian daily note. It is intended for users who explicitly want an agent to append concise Markdown timeline entries to a local Obsidian vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill appends activity data to a local Obsidian daily note, which can persist personal location, travel, schedule, and activity details. <br>
Mitigation: Use explicit save or log wording before execution and review the entries that will be written, especially in shared chats. <br>
Risk: The updater defaults to a hard-coded Windows Obsidian vault path. <br>
Mitigation: Confirm that the configured daily note directory and template path match the user's machine before running the script. <br>
Risk: Ambiguous group-chat messages could be mistaken for content that should be saved. <br>
Mitigation: Require a clear trigger such as /dailylog, /travellog, /timeline, or a direct save-to-Obsidian request; ask for confirmation when intent is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freznel10/obsidian-daily-log) <br>
- [Publisher profile](https://clawhub.ai/user/freznel10) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown timeline entries and Python command invocations that append to a local Obsidian daily note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The updater writes chronological bullet or table entries into a ## Timeline section and avoids duplicate identical lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
