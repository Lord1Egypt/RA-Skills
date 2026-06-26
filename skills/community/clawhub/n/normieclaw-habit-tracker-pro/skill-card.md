## Description: <br>
Habit Tracker Pro turns an AI agent into a conversational accountability partner for daily habits with check-ins, streak tracking, pattern analysis, exports, dashboard widgets, and local cross-tool sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to configure conversational habit tracking, daily check-ins, streak summaries, weekly reports, local exports, and lightweight dashboard views for personal routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit names, completion records, skip reasons, notes, and pattern analysis can reveal sensitive health, sleep, work, or routine information. <br>
Mitigation: Review the data stored under ~/.normieclaw/habit-tracker-pro/ before use, avoid entering sensitive freeform notes, and delete local data or exports when they are no longer needed. <br>
Risk: Recurring automated check-ins may expose private routine details through the configured chat channel. <br>
Mitigation: Use only trusted chat channels and hosting environments, and disable or adjust check-in schedules if the channel is shared or monitored. <br>
Risk: Cross-tool sync can share habit completion data with other local NormieClaw tools. <br>
Mitigation: Enable integrations only when needed, confirm which tools can read or write habit data, and disable sync paths that are not required. <br>
Risk: Export scripts create CSV and markdown files that may duplicate personal habit data. <br>
Mitigation: Store exports in a protected location, share them cautiously, and remove exported files separately from the main data directory when deleting records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/normieclaw-habit-tracker-pro) <br>
- [README](artifact/README.md) <br>
- [Security considerations](artifact/SECURITY.md) <br>
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, local files, CSV exports, and markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local habit data under ~/.normieclaw/habit-tracker-pro/ and optional CSV/markdown exports.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
