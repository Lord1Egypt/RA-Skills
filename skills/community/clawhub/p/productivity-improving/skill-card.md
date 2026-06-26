## Description: <br>
Productivity tracker and daily review assistant. Input activity logs, time notes, goals, or a daily schedule; output time categories, bottlenecks, focus leaks, and next-day actions. Works from user-provided data and does not require account access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to record activities, categorize time, review productivity patterns, and generate daily or weekly summaries from user-provided work and life activity logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Activity history may include sensitive personal or work details and is stored locally in plain JSON and Markdown files. <br>
Mitigation: Use explicit /track commands for intended entries, avoid logging sensitive details, and manually delete or manage the local data directory when long-term history is not desired. <br>


## Reference(s): <br>
- [Skill Source](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/productivity-improving) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, guidance] <br>
**Output Format:** [Plain text responses, Markdown reports, JSON activity data, and CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores activity history and generated logs locally unless the user exports or connects optional integrations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
