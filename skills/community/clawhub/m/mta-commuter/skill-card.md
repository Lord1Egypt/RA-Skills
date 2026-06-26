## Description: <br>
NYC commuter transit for LIRR, Metro-North, and Subway schedules, trip planning, service alerts, nearby stations, alternatives, and track alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ottomanelli](https://clawhub.ai/user/ottomanelli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer NYC-area commuter transit questions, plan LIRR, Metro-North, and Subway trips, check service alerts, and set optional track-assignment watches. <br>

### Deployment Geography for Use: <br>
United States (New York metropolitan area) <br>

## Known Risks and Mitigations: <br>
Risk: Saved places such as home and work can be stored locally in data/locations.json. <br>
Mitigation: Only save locations the user explicitly provides and remind users where local saved-location data is stored. <br>
Risk: User-provided addresses may be geocoded through the agent's web or geocoding path. <br>
Mitigation: Confirm the user's intent before geocoding sensitive addresses and avoid sharing unnecessary address detail. <br>
Risk: Track watch can create a temporary cron poller for a specific train. <br>
Mitigation: Use track watch only on explicit request and make clear how the watch is removed or allowed to auto-delete. <br>
Risk: Track watch depends on unofficial mylirr.org and mymnr.org endpoints that may change or become unavailable. <br>
Mitigation: Treat track assignments as best-effort and fall back to official MTA feeds or station information when the watch endpoint fails. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ottomanelli/mta-commuter) <br>
- [Project Homepage](https://github.com/ottomanelli/mta-commuter) <br>
- [MTA Developer Resources](https://new.mta.info/developers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated CLI commands for MTA lookups and optional OpenClaw cron setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
