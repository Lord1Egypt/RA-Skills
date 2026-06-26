## Description: <br>
Income Tracker records multi-platform income and provides statistics, trend charts, source analysis, data export, and simple forecasting for freelancers, creators, and side-business users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as freelancers, creators, and side-business operators use this skill to record income from multiple sources, summarize earnings over time, analyze source mix, export records, and review simple income projections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Income history, notes, and client details may be sensitive because records are stored in a local JSON file. <br>
Mitigation: Use a dedicated private DATA_PATH and protect the file with filesystem permissions or disk encryption. <br>
Risk: Currency conversion and forecast values may be inaccurate because the skill uses fixed exchange rates and simple projections. <br>
Mitigation: Treat converted totals and projections as approximate and verify them before financial reporting or business decisions. <br>
Risk: Local JSON data may be lost or edited outside the skill. <br>
Mitigation: Back up the data file regularly and review manual edits before relying on reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/income-tracker-zhouli) <br>
- [Clawdis homepage](https://clawhub.com/skills/income-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, CSV, Configuration, Guidance] <br>
**Output Format:** [JSON responses with income records, summaries, ASCII charts, CSV/JSON exports, and concise recommendation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores income records in a local JSON file selected by DATA_PATH or the default user data path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, frontmatter, package.json, skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
