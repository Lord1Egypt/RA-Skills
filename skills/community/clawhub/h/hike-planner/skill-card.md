## Description: <br>
一站式徒步出行规划：生成含徒步路线、交通、住宿、人文和装备的完整行程计划，支持 GPX/KML 轨迹解析与地图渲染。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[updatedb](https://clawhub.ai/user/updatedb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to plan hiking trips, compare routes, assemble transportation and lodging details, parse GPX/KML tracks, and maintain local itinerary state. It is designed for user-directed planning and does not book tickets, place orders, join waitlists, or make payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags under-scoped local file access and unsafe command execution paths. <br>
Mitigation: Use a dedicated output directory, avoid providing paths to unrelated private files, and review local helper command behavior before installation or execution. <br>
Risk: The skill can persist itinerary, order, media, and route data locally. <br>
Mitigation: Store outputs in a location intended for travel planning data and review saved files before sharing or archiving them. <br>
Risk: Generated map links and HTML can contain precise route coordinates or trip locations. <br>
Mitigation: Treat generated maps and links as sensitive location data and share them only with intended recipients. <br>
Risk: The skill uses a sensitive Amap credential for map and geocoding workflows. <br>
Mitigation: Provide only the required AMAP_WEBSERVICE_KEY value and manage it outside shared itinerary outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/updatedb/hike-planner) <br>
- [Hike Planner SOP](references/hike-planner-sop.md) <br>
- [Plan Template](references/PLAN_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown itinerary plans, JSON route statistics, HTML map files, and command/configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist itinerary state, generated plans, parsed route data, and map artifacts in the configured output directory.] <br>

## Skill Version(s): <br>
3.3.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
