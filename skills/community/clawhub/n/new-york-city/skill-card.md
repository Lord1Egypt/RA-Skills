## Description:

Navigate New York City for visits, moves, neighborhoods, transit, housing, food, work, and daily street-level decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get practical New York City guidance for visiting, moving, living, working, or studying in the city. It helps tailor advice around boroughs, neighborhoods, transit, housing, food, safety, weather, and daily logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional local memory under ~/new-york-city/ may store personal context in plaintext.

Mitigation: Store only coarse planning details and avoid saving passwords, account numbers, passport details, payment information, or exact home addresses.

Risk: Some NYC rules, fares, policies, and service workflows change over time.

Mitigation: Verify precise operational guidance against official city, transit, airport, venue, or agency sources before relying on it.

Risk: Location-specific guidance may send borough, ZIP, station, or airport context to official public websites.

Mitigation: Send location context only when the user asks for location-specific help and is comfortable with that lookup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/new-york-city)
- [Skill Homepage](https://clawic.com/skills/new-york-city)
- [NYC Official Portal](https://www.nyc.gov/)
- [NYC 311](https://www.nyc.gov/311)
- [NYC Housing Information](https://www.nyc.gov/site/hpd/index.page)
- [Metropolitan Transportation Authority](https://new.mta.info/)
- [OMNY](https://omny.info/)
- [Port Authority of New York and New Jersey](https://www.panynj.gov/)
- [NYC Ferry](https://www.ferry.nyc/)
- [Official NYC Tourism Portal](https://www.nyctourism.com/)
- [NYC Parks](https://www.nycgovparks.org/)
- [Official Sources Map](artifact/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with occasional inline shell commands or configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally use local plaintext memory under ~/new-york-city/ after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
