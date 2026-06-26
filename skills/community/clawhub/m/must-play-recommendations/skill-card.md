## Description: <br>
Recommends must-play city attractions by combining FlyAI CLI results for 5A-rated scenic areas and popular well-reviewed points of interest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ysxiiun](https://clawhub.ai/user/ysxiiun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to answer city attraction requests with ranked Markdown recommendations, ticket notes, addresses, travel guidance, and booking links from FlyAI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City and travel-search queries are sent to the external FlyAI/Feizhu travel service. <br>
Mitigation: Avoid including sensitive itinerary details unless they are necessary for the recommendation request. <br>
Risk: A configured FlyAI API key is a credential that could require rotation if exposed. <br>
Mitigation: Store the key in the expected FlyAI configuration only, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: The bundled FlyAI reference covers broader travel actions beyond attraction recommendations. <br>
Mitigation: Use this skill for attraction recommendations rather than booking, flight, hotel, or account-related actions. <br>


## Reference(s): <br>
- [FlyAI CLI Reference](flyai-readme.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ysxiiun/must-play-recommendations) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown attraction recommendations with inline FlyAI CLI command examples and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a city name as required input and may include images, ticket information, addresses, travel guidance, and external booking URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
