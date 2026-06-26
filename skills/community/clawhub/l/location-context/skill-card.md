## Description: <br>
Get comprehensive context about a location including nearby places, area description, and optional weather. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[James-southendsolutions](https://clawhub.ai/user/James-southendsolutions) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to provide location-aware context, including nearby places, area descriptions, tailored local recommendations, and optional weather context for trip planning, meeting locations, and outdoor activity planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided location details to the Camino API. <br>
Mitigation: Use it only when sharing the submitted location details with Camino is acceptable. <br>
Risk: The skill requires a CAMINO_API_KEY in the local environment. <br>
Mitigation: Store the API key in the agent environment and avoid placing it in prompts, shell history, or shared files. <br>
Risk: The skill documentation recommends optional companion skills. <br>
Mitigation: Review and assess any companion skills separately before installing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/James-southendsolutions/location-context) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino Context API endpoint](https://api.getcamino.ai/context) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown usage guidance and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY and sends user-provided location details to the Camino API.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
