## Description: <br>
Provides Hong Kong hiking route recommendations, Shenzhen border-crossing connections, weather assessment, facility lookup, and safety guidance for hiking planning, equipment, camping supplies, and weather-risk questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaydontse23](https://clawhub.ai/user/jaydontse23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to plan Hong Kong hikes, compare trail difficulty and timing, connect from Shenzhen border crossings, check facilities, and frame weather or safety decisions before a trip. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Static trail, facility, route-time, and transport information may be stale or incomplete at the time of an actual hike. <br>
Mitigation: Verify current Hong Kong Observatory warnings, official trail and facility status, transport changes, daylight, water needs, equipment, and emergency plans before departure. <br>
Risk: Route recommendations can be inappropriate if user fitness, weather, daylight, or equipment constraints are missing. <br>
Mitigation: Collect the planned route or desired route type, departure date, starting point, available time, group fitness, camping plans, and tolerance for exposed or steep terrain before giving firm recommendations. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/jaydontse23/hkhiking) <br>
- [Hong Kong four major hiking trails](references/trails.md) <br>
- [Additional Hong Kong hiking routes](references/more-trails.md) <br>
- [Shenzhen to Hong Kong hiking transport](references/transport.md) <br>
- [Hong Kong weather and hiking safety](references/weather-safety.md) <br>
- [Country park facilities](references/country-park-facilities.md) <br>
- [Hong Kong Observatory weather API](https://data.weather.gov.hk/weatherAPI/opendata/weather.php) <br>
- [Hong Kong Observatory hiking weather service](https://www.hko.gov.hk/tc/sports/index.html) <br>
- [Hiking route GeoJSON data](https://www.hko.gov.hk/hiking/geojson/walks.geojson) <br>
- [AFCD campsite dataset](https://data.gov.hk/tc-data/dataset/hk-afcd-afcdlist-campsite) <br>
- [AFCD water dispenser dataset](https://data.gov.hk/tc-data/dataset/hk-afcd-afcdlist-water-dispenser) <br>
- [AFCD toilet dataset](https://data.gov.hk/tc-data/dataset/hk-afcd-afcdlist-toilet) <br>
- [Fortune Ferry ETA dataset](https://data.gov.hk/tc-data/dataset/ff-fortune-schedule2/resource/7a5fb82f-129e-4acc-9346-b97e61093ab4) <br>
- [Hong Kong and Kowloon Ferry data](https://data.gov.hk/tc-data/dataset/hkkf-hkkfdata-hkkf-eta-data) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API Calls] <br>
**Output Format:** [Markdown with structured route, transport, facility, weather, equipment, and safety recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public API lookup snippets or source links for users to verify live weather, transport, and facility status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
