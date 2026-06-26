## Description: <br>
Austrian rail travel planner (ÖBB Scotty) for planning rail journeys, checking station departures and arrivals, and reviewing service disruptions across ÖBB trains, S-Bahn, regional trains, and neighboring-country connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manmal](https://clawhub.ai/user/manmal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and travel-support agents use this skill to query ÖBB Scotty for station lookup, journey planning, station boards, and current public-transport disruptions in Austria and nearby cross-border routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Station names, trip dates, times, and route queries are sent to the ÖBB Scotty API. <br>
Mitigation: Use normal public-transport inputs and avoid submitting sensitive personal itinerary details. <br>
Risk: The helper scripts depend on local bash, curl, and jq execution. <br>
Mitigation: Install these tools from trusted system packages and review commands before running them. <br>


## Reference(s): <br>
- [ÖBB Scotty HAFAS mgate API endpoint](https://fahrplan.oebb.at/bin/mgate.exe) <br>
- [ClawHub release page](https://clawhub.ai/manmal/oebb-scotty) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bash, curl, and jq to return station matches, trip summaries, station-board results, and disruption records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
