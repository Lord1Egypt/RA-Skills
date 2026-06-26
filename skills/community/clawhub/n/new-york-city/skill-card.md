## Description: <br>
Navigate New York City for visits, moves, neighborhoods, transit, housing, food, work, and daily street-level decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for practical New York City guidance across visits, relocation, resident life, work, and study. It helps route advice around borough, neighborhood, commute, housing, food, airport, safety, weather, and city-service constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use optional local memory for boroughs, neighborhoods, commute constraints, budget pressure, timelines, and open tasks. <br>
Mitigation: Use stateless mode if local files are not desired, and create or update ~/new-york-city/ only after user confirmation. <br>
Risk: Precise New York City rules, fares, service workflows, and route details can change. <br>
Mitigation: Verify operational details against official city, transit, airport, venue, or agency sources before giving precise steps. <br>
Risk: Local memory could contain sensitive details if a user stores more than the skill needs. <br>
Mitigation: Do not store credentials, payment details, passport numbers, account numbers, or full street addresses in the memory file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/new-york-city) <br>
- [Skill homepage](https://clawic.com/skills/new-york-city) <br>
- [NYC official portal](https://www.nyc.gov/) <br>
- [NYC 311](https://www.nyc.gov/311) <br>
- [NYC housing information](https://www.nyc.gov/site/hpd/index.page) <br>
- [Metropolitan Transportation Authority](https://new.mta.info/) <br>
- [OMNY](https://omny.info/) <br>
- [Port Authority of New York and New Jersey](https://www.panynj.gov/) <br>
- [NYC Ferry](https://www.ferry.nyc/) <br>
- [Official NYC tourism portal](https://www.nyctourism.com/) <br>
- [NYC Parks](https://www.nycgovparks.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with optional local memory structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of optional local notes under ~/new-york-city/ only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
