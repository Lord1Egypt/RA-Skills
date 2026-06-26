## Description: <br>
Check Dutch train schedules, departures, disruptions, and plan journeys using the NS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eggressive](https://clawhub.ai/user/eggressive) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to ask an agent for Dutch train journey planning, station lookup, arrivals, departures, active disruptions, and commute checks backed by the official NS API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Station names, routes, and optional commute locations are sent to the NS API and may reveal travel intent. <br>
Mitigation: Use the skill only when sharing those queries with the NS API is acceptable; avoid setting NS_HOME_STATION or NS_WORK_STATION if persistent commute locations are sensitive. <br>
Risk: The NS subscription key is required for API access and could be exposed if committed or pasted into shared logs. <br>
Mitigation: Provide NS_SUBSCRIPTION_KEY through a runtime secret mechanism, do not commit it, and rotate the key in the NS API portal if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eggressive/ns-trains) <br>
- [NS API Portal](https://apiportal.ns.nl/) <br>
- [NS API Starter Guide](https://apiportal.ns.nl/startersguide) <br>
- [Security Notes](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output with setup guidance and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an NS_SUBSCRIPTION_KEY environment variable; optional commute shortcuts use NS_HOME_STATION and NS_WORK_STATION.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
