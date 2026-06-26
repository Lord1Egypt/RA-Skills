## Description: <br>
Provides a real-time local dashboard with weather, air quality, currency exchange rates, holidays, moon phase, and contextual tips for a selected city. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PEDROHENRIQUE202525](https://clawhub.ai/user/PEDROHENRIQUE202525) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users ask an agent for a city-level daily status summary. The skill guides the agent to collect public weather, astronomy, exchange-rate, holiday, and air-quality signals and present them as a Portuguese dashboard. <br>

### Deployment Geography for Use: <br>
Brazil <br>

## Known Risks and Mitigations: <br>
Risk: City-level location and related local queries are sent to public third-party services. <br>
Mitigation: Use the skill only when city-level sharing is acceptable, and avoid including more precise location or personal data in the query. <br>
Risk: The skill instructs the agent to run curl commands with a user-provided city value. <br>
Mitigation: Encode the city as URL data, avoid placing raw user input into shell commands, and prefer a safer HTTP request tool when available. <br>


## Reference(s): <br>
- [wttr.in weather service](https://wttr.in/) <br>
- [AwesomeAPI currency API](https://docs.awesomeapi.com.br/api-de-moedas) <br>
- [Nager.Date public holidays API](https://date.nager.at/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown containing a fenced plain-text ASCII dashboard in Portuguese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a city name input and defaults to Goiania when the city is omitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
