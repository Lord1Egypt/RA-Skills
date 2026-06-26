## Description: <br>
Chicago Metra commuter rail -- real-time train arrivals, vehicle tracking, service alerts, and schedule info for all 11 Metra lines serving the Chicago metropolitan area. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianleach](https://clawhub.ai/user/brianleach) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and transit-focused agents use this skill to answer Chicago Metra questions about train arrivals, vehicle positions, service alerts, schedules, routes, stops, and fares. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Metra API key for realtime feeds. <br>
Mitigation: Use a dedicated Metra API key and keep unrelated secrets out of the skill-local .env file. <br>
Risk: Installation runs npm install for the protobuf dependency. <br>
Mitigation: Review package.json and package-lock.json before installing dependencies in the target environment. <br>
Risk: The skill writes public GTFS schedule data to a local cache under ~/.metra/gtfs. <br>
Mitigation: Allow the cache only in environments where local storage of public schedule data is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianleach/metra) <br>
- [Metra developer documentation](https://metra.com/developers) <br>
- [Metra GTFS realtime API base](https://gtfspublic.metrarr.com) <br>
- [Metra static GTFS schedule feed](https://schedules.metrarail.com/gtfs/schedule.zip) <br>
- [Metra GTFS published timestamp](https://schedules.metrarail.com/gtfs/published.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-oriented text with inline shell commands and transit results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require live API calls to Metra GTFS realtime feeds and local GTFS static data cached under ~/.metra/gtfs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
