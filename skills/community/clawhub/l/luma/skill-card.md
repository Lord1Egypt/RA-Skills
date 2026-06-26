## Description: <br>
Fetch upcoming events from Luma (lu.ma) for any city. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regalstreak](https://clawhub.ai/user/regalstreak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to find upcoming Luma events, tech meetups, startup events, conferences, and networking opportunities by city. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched event data may create a privacy-relevant local cache of searched cities, event interests, or possible plans. <br>
Mitigation: Review or delete ~/clawd/memory/luma-events.json when retained event search history is not desired. <br>
Risk: Results depend on public Luma pages and may become stale or fail if Luma changes page structure or event availability. <br>
Mitigation: Refresh results before relying on event times, locations, ticket status, or attendance details. <br>


## Reference(s): <br>
- [ClawHub Luma Events release page](https://clawhub.ai/regalstreak/luma) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Human-readable text or JSON event listings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes event names, venues, dates, hosts, guest counts, ticket status, and Luma links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
