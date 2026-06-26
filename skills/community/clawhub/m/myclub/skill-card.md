## Description: <br>
Fetch sports schedules, practices, games, and events from myclub.fi accounts with locally stored credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanninen](https://clawhub.ai/user/hanninen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to discover myclub.fi accounts and fetch upcoming practices, games, tournaments, and other club events as readable schedule summaries or structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores myclub.fi credentials locally. <br>
Mitigation: Install only on a trusted machine, keep the local config file private, and remove ~/.myclub-config.json when the skill is no longer needed. <br>
Risk: Optional debug output can leave authenticated pages and session cookies in local files. <br>
Mitigation: Avoid debug mode unless troubleshooting, and delete any /tmp/myclub-* debug files after use. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/hanninen/myclub-skill) <br>
- [myclub.fi](https://myclub.fi) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text summaries or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes event names, venues, dates, times, categories, groups, and registration status when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
