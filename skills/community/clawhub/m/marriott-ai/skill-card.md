## Description: <br>
MarriottAI helps agents search, compare, and book Marriott hotels, hotel packages, nearby attractions, and train tickets through the FlyAI travel CLI with real-time pricing and structured results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[birkhoff-china](https://clawhub.ai/user/birkhoff-china) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users and travel-support agents use this skill to find Marriott stays, package offers, nearby attractions, and train options, then present booking-oriented comparisons and itinerary guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses a third-party FlyAI npm CLI that may handle travel search details and optional API credentials. <br>
Mitigation: Install only when comfortable with that data flow, and use a limited FLYAI_API_KEY where possible. <br>
Risk: Returned prices, package details, and booking links may reflect a limited source set or change before purchase. <br>
Mitigation: Compare prices, terms, and availability with other sources before booking when neutrality or broad market coverage matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/birkhoff-china/marriott-ai) <br>
- [FlyAI homepage](https://open.fly.ai/) <br>
- [Marriott hotel search reference](references/search-marriott-hotel.md) <br>
- [Marriott package search reference](references/search-marriott-package.md) <br>
- [POI and attraction search reference](references/search-poi.md) <br>
- [Train search reference](references/search-train.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Single-line JSON from CLI commands, with Markdown result summaries for users.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the @fly-ai/flyai-cli package; FLYAI_API_KEY is optional for enhanced results.] <br>

## Skill Version(s): <br>
1.0.6 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
