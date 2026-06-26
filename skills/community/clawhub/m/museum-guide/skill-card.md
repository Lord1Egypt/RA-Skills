## Description: <br>
Museum Guide helps an agent plan museum visits by extracting visitor preferences, finding relevant artifacts from offline museum CSV data or online search, and producing an ordered itinerary with must-see highlights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangmingchen1994-dotcom](https://clawhub.ai/user/yangmingchen1994-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan efficient museum visits based on the museum name, visit duration, child-friendly needs, interests, artifact types, and dynasty preferences. It returns a confirmation step first, then a route with prioritized artifacts, reasons, and basic visit information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Museum requests, preferences, and possible family-travel details may be sent to the configured LLM provider. <br>
Mitigation: Use a trusted LLM endpoint, configure a dedicated API key, and avoid entering sensitive personal details. <br>
Risk: Online fallback can send museum search queries through the configured local ProSearch proxy when no offline CSV is available. <br>
Mitigation: Prefer the bundled offline CSV data when possible and confirm that AUTH_GATEWAY_PORT points to an expected local service before using online search. <br>
Risk: Generated opening hours, ticket, transit, or facility details may be incomplete or outdated. <br>
Mitigation: Check the museum's official site before visiting, especially for time-sensitive logistics. <br>


## Reference(s): <br>
- [Museum Guide ClawHub release](https://clawhub.ai/yangmingchen1994-dotcom/museum-guide) <br>
- [中国国家博物馆.csv](references/中国国家博物馆.csv) <br>
- [上海博物馆.csv](references/上海博物馆.csv) <br>
- [故宫珍宝馆.csv](references/故宫珍宝馆.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON confirmation output followed by a Markdown museum itinerary with tables and visit guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a two-phase flow: show the confirmation prompt before running route generation.] <br>

## Skill Version(s): <br>
1.4.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
