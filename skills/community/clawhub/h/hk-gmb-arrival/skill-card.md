## Description: <br>
Real-time arrival information for Hong Kong Green Mini Buses (GMB). Supports fuzzy stop name matching and multi-region route lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenho1394](https://clawhub.ai/user/stevenho1394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and transit-focused agents use this skill to search Hong Kong Green Minibus routes and retrieve the next arrivals for a route, direction, stop, and region. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public Hong Kong transit data services, so API outages or response changes can affect arrival lookups. <br>
Mitigation: Keep network failures surfaced as JSON errors and use short-lived caching for ETA responses to reduce repeated calls. <br>
Risk: Cached public transit JSON is stored locally in the skill data directory and could become stale or misleading if modified outside the skill. <br>
Mitigation: Keep cache files scoped to the skill directory, honor TTLs, and rely on host file permissions to protect cached data. <br>
Risk: Route, direction, stop, and region inputs determine which public API requests are made. <br>
Mitigation: Preserve strict validation for route format, direction values, and HKI/KLN/NT region codes before making requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenho1394/hk-gmb-arrival) <br>
- [Official Hong Kong GMB ETA API](https://data.etagmb.gov.hk) <br>
- [HK Bus route fare list](https://data.hkbus.app/routeFareList.min.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns route-region matches, stop identifiers, stop names, up to three arrival times, errors, messages, or suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
