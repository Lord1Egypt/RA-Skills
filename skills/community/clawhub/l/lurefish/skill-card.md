## Description: <br>
Lurefish helps anglers plan lure-fishing trips, record catches, check weather and tides, choose lures, and summarize catch history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeansgit](https://clawhub.ai/user/jeansgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and fishing hobbyists use this skill to decide when and where to fish, select suitable lure-fishing bait, record catch details, and review catch statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Catch logs can include fishing locations, notes, dates, and statistics stored locally under ~/lurefish. <br>
Mitigation: Avoid entering sensitive locations or notes, and review or delete ~/lurefish when records should no longer be retained. <br>
Risk: Weather, tide, map, or spot recommendations may use online lookups and can disclose query locations to external services. <br>
Mitigation: Provide weather or tide information manually when privacy matters, and review suggested searches before running them. <br>
Risk: Fishing guidance can be incomplete or inaccurate for local law, access restrictions, safety conditions, or species rules. <br>
Mitigation: Check current local regulations, site access, weather, water conditions, and safety requirements before fishing. <br>


## Reference(s): <br>
- [Lure Knowledge](references/lures.md) <br>
- [Target Species](references/species.md) <br>
- [ClawHub Release Page](https://clawhub.ai/jeansgit/lurefish) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional JSON catch records and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and read local JSON files under ~/lurefish when scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
