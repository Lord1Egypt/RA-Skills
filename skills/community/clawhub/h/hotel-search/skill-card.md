## Description: <br>
Search Google Hotels for hotel prices, ratings, and availability using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillhq-ai](https://clawhub.ai/user/skillhq-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search Google Hotels, compare hotel prices, ratings, amenities, and availability, and receive summarized accommodation options without completing a booking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can optionally leave Google Hotels for hotel or promo-code sites after presenting results. <br>
Mitigation: Ask the user before visiting external hotel sites and avoid signing in, entering payment details, or continuing beyond research unless the user explicitly requests it. <br>
Risk: Hotel prices and availability are real-time and may change before booking. <br>
Mitigation: Present prices as indicative research results and tell the user to verify current terms on the booking site before making a purchase. <br>
Risk: Browser automation may encounter consent screens, CAPTCHAs, or stale page state. <br>
Mitigation: Use fresh snapshots after interactions, do not solve CAPTCHAs, and stop with a clear explanation when automation is blocked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skillhq-ai/hotel-search) <br>
- [Google Hotels interaction patterns](references/interaction-patterns.md) <br>
- [agent-browser](https://github.com/nicobailey/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with hotel comparison tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser automation through agent-browser and should not complete purchases or enter payment details.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
