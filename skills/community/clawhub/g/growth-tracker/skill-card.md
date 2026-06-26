## Description: <br>
Growth Tracker produces quantified progress reports for growth, tasks, learning, efficiency, achievements, and goals using local metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to track and summarize AI and user progress across daily work, learning, efficiency, achievements, and goals. It is useful when users want numeric reports, comparisons, goal updates, exports, or resets for locally stored progress data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains a local history of progress, task, learning, achievement, and goal metrics. <br>
Mitigation: Review ~/.openclaw/data/quantified_self.json periodically and reduce retention_days or disable auto_track if ongoing local profiling is not desired. <br>
Risk: Export and reset workflows can expose or remove locally stored progress data. <br>
Mitigation: Use export and reset commands deliberately, and confirm the target file before sharing, deleting, or reinitializing local data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shianaixuexi-cell/growth-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/shianaixuexi-cell) <br>
- [README](artifact/README.md) <br>
- [Data template](artifact/data-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with progress metrics, tables, inline shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON export/reset guidance for the quantified_self data file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
