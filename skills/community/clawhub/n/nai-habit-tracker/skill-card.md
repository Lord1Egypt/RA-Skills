## Description: <br>
Track daily habits, streaks, and completions locally with JSON-backed CLI scripts and weekly Markdown reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add, archive, log, check, and review personal habits through local Python CLI scripts without external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit names, completion history, and review notes are stored locally and may reveal personal routines. <br>
Mitigation: Use non-sensitive habit names when privacy matters and store habit data only in trusted local directories. <br>
Risk: The skill can create and update local habit JSON files and optional Markdown review files. <br>
Mitigation: Review the intended command and data or output path before execution; use HABIT_DATA_DIR, --data-dir, or --output only with directories the user intends to modify. <br>


## Reference(s): <br>
- [Habit Tracker Data Format](references/data-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/nai-habit-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON status output, and Markdown weekly review reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON habit files and optional Markdown output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
