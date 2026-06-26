## Description: <br>
Provides Amap-based geocoding, reverse geocoding, nearby place search, route planning, venue details, and map link generation for mainland China travel and location workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhijun](https://clawhub.ai/user/lizhijun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and travel-planning agents use this skill to resolve mainland China addresses, search nearby points of interest, plan routes, inspect venue details, and generate navigation links through LovTrip and Amap services. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The fallback shell script can run unintended local code when crafted address, city, or keyword text is passed to it. <br>
Mitigation: Prefer the MCP path from a pinned, trusted LovTrip package version and avoid scripts/amap.sh with untrusted address, city, or keyword text until its quoting is fixed. <br>
Risk: The skill sends location, route, and venue queries to external map services. <br>
Mitigation: Use a restricted Amap API key and avoid submitting highly sensitive home, work, or travel locations unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lizhijun/lovtrip-china-map) <br>
- [LovTrip](https://lovtrip.app) <br>
- [LovTrip Developer Documentation](https://lovtrip.app/developer) <br>
- [LovTrip Planner](https://lovtrip.app/planner) <br>
- [Amap Tool Parameter Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON API results and map links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AMAP_API_KEY for Amap requests; generated results may include location data, route details, venue metadata, and navigation URLs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
