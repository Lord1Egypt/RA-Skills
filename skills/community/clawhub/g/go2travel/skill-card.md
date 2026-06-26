## Description: <br>
go2Travel helps agents plan trips with Fliggy travel data, including itineraries, flights, hotels, attractions, budgets, and travel support tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonhuohuo](https://clawhub.ai/user/jasonhuohuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan leisure, family, business, pet-friendly, outdoor, and multi-city travel. It supports itinerary planning, Fliggy-backed flight, hotel, attraction, food, and rental-car searches, budget comparison, packing, visa, insurance, route, weather, and practical travel guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel searches use configured flyai access and external travel services, and weather or exchange-rate requests may disclose destination or query details to external services. <br>
Mitigation: Install and use the skill only when that external service use is acceptable, and avoid sending sensitive personal details in travel queries. <br>
Risk: Prices, availability, travel policies, visa, health, weather, and emergency information can become outdated or incomplete. <br>
Mitigation: Treat generated plans as planning assistance and verify time-sensitive or high-impact details with official providers before booking, traveling, or making safety decisions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jasonhuohuo/go2travel) <br>
- [Fly AI homepage](https://open.fly.ai/) <br>
- [Role index](references/roles-index.md) <br>
- [Keyword search reference](references/keyword-search.md) <br>
- [Flight search reference](references/search-flight.md) <br>
- [Hotel search reference](references/search-hotel.md) <br>
- [POI search reference](references/search-poi.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables, links, images when available, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Fliggy prices, images, and booking links when returned by the flyai CLI; time-sensitive travel details should be verified before booking or acting.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
