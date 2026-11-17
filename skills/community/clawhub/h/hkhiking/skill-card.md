## Description:

Provides Hong Kong hiking route recommendations, Shenzhen-to-Hong Kong access guidance, weather risk assessment, facilities lookup, and safety advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaydontse23](https://clawhub.ai/user/jaydontse23)

### License/Terms of Use:

MIT-0

## Use Case:

External users and hiking planners use this skill to choose Hong Kong hiking routes, plan access from Shenzhen or local transit, assess weather and trail risks, and check facilities such as campsites, toilets, water points, and return options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather warnings, route closures, facility availability, and transit or ferry details may change after the skill's reference data is consulted.

Mitigation: Verify current Hong Kong Observatory warnings, official closure notices, facility pages, and operator schedules before hiking.

Risk: Route difficulty and time estimates can be misleading if the user's fitness, group composition, or date is unknown.

Mitigation: Collect the route, date, starting point, available time, fitness level, group needs, and camping plans before giving final recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaydontse23/skills/hkhiking)
- [Hong Kong Four Major Hiking Trails](references/trails.md)
- [Hong Kong Additional Hiking Routes](references/more-trails.md)
- [Shenzhen-to-Hong Kong Hiking Transport](references/transport.md)
- [Hong Kong Weather and Hiking Safety](references/weather-safety.md)
- [Country Park Facilities](references/country-park-facilities.md)
- [Hong Kong Observatory Weather API](https://data.weather.gov.hk/weatherAPI/opendata/weather.php)
- [Hong Kong Observatory Hiking Trail GeoJSON](https://www.hko.gov.hk/hiking/geojson/walks.geojson)
- [AFCD Campsite Dataset](https://data.gov.hk/tc-data/dataset/hk-afcd-afcdlist-campsite)
- [AFCD Water Dispenser Dataset](https://data.gov.hk/tc-data/dataset/hk-afcd-afcdlist-water-dispenser)
- [AFCD Toilet Dataset](https://data.gov.hk/tc-data/dataset/hk-afcd-afcdlist-toilet)
- [Fortune Ferry ETA Dataset](https://data.gov.hk/tc-data/dataset/ff-fortune-schedule2/resource/7a5fb82f-129e-4acc-9346-b97e61093ab4)
- [Hong Kong and Kowloon Ferry Data](https://data.gov.hk/tc-data/dataset/hkkf-hkkfdata-hkkf-eta-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown route plans and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route comparisons, transit steps, weather-risk caveats, facility notes, and equipment or supply recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
