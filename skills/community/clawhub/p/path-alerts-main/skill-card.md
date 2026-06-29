## Description: <br>
Get real-time NJ PATH train service alerts, delays, status updates, and live arrival times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liamsx45](https://clawhub.ai/user/liamsx45) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check NJ PATH service disruptions, line status, and live station arrivals from public transit feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transit status and arrival output depends on external public feeds that may be unavailable, stale, or incomplete. <br>
Mitigation: Treat results as advisory and verify critical travel decisions against official PATH or Port Authority channels. <br>
Risk: The artifact performs network requests to public transit endpoints. <br>
Mitigation: Run it in an environment where outbound access to those feeds is expected and review network permissions before deployment. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/LiamSx45/openclaw-path-alerts) <br>
- [Port Authority alerts feed](https://www.panynj.gov/bin/portauthority/everbridge/incidents) <br>
- [PATH GTFS-Realtime feed](https://path.transitdata.nyc/gtfsrt) <br>
- [ClawHub skill page](https://clawhub.ai/liamsx45/path-alerts-main) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown-formatted status and arrival messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public PATH alerts and GTFS-Realtime feeds; no API keys are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
