## Description: <br>
Searches hotel availability and pricing by city, dates, and guest count using the Amadeus API and returns JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrojas537](https://clawhub.ai/user/jrojas537) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and travel-planning users use this skill to configure Amadeus API credentials and search hotel offers from a CLI by IATA city code, stay dates, guests, and radius. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amadeus API credentials and cached access tokens are stored locally without clearly documented or enforced secret-storage protections. <br>
Mitigation: Use a private account, avoid shared or synced home directories, ensure ~/.config/hotel-pricer/config.yaml is readable only by your user, and rotate the Amadeus secret if it may have been exposed. <br>


## Reference(s): <br>
- [Hotel Pricer on ClawHub](https://clawhub.ai/jrojas537/hotel-pricer) <br>
- [Amadeus for Developers](https://developers.amadeus.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the hotel search command, with Markdown guidance and shell commands for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Amadeus API credentials and network access to the Amadeus test API.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
