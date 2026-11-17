## Description:

go2Travel helps agents plan trips, build itineraries, and search flights, hotels, attractions, food, rental cars, visas, budgets, packing needs, and other travel details using Fly/Fliggy travel data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonhuohuo](https://clawhub.ai/user/jasonhuohuo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to turn travel requests into concise itineraries with transportation, lodging, daily activities, budget notes, and follow-up travel guidance. It can also support narrower travel tasks such as flight, hotel, attraction, restaurant, rental car, visa, packing, weather, currency, insurance, emergency, photography, and itinerary-review questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents raw shell and network command templates that include user-controlled destinations or queries.

Mitigation: Review commands before execution, keep user values quoted as arguments, and run the skill where shell execution can be sandboxed or approved.

Risk: The skill relies on a globally installed, unpinned npm CLI for live Fliggy data.

Mitigation: Pin and audit the flyai CLI version in deployment, and restrict network access to the expected travel-data endpoints.

Risk: Health and medication suggestions could be mistaken for medical advice.

Mitigation: Treat health output as general travel preparation and direct users to qualified medical care for symptoms, prescriptions, or urgent issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonhuohuo/skills/go2travel)
- [Fly AI homepage](https://open.fly.ai/)
- [flyai CLI source](https://github.com/alibaba-flyai/flyai-skill)
- [Roles index](artifact/references/roles-index.md)
- [keyword-search reference](artifact/references/keyword-search.md)
- [search-flight reference](artifact/references/search-flight.md)
- [search-hotel reference](artifact/references/search-hotel.md)
- [search-poi reference](artifact/references/search-poi.md)
- [Security documentation](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel plans, tables, checklists, links, image references, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live travel prices, public booking links, weather or currency data, and role-specific follow-up prompts when available.]

## Skill Version(s):

2.0.6 (source: server release evidence; artifact metadata reports 2.0.3 and artifact changelog top entry is v1.9.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
