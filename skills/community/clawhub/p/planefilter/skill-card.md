## Description: <br>
Aviation flight lookup skill for querying aircraft type, equipment changes, and confidence scoring for a flight number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImL1s](https://clawhub.ai/user/ImL1s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel, operations, and aviation users can ask an agent to look up the aircraft assigned to a flight, detect possible equipment changes, and explain confidence from multiple aviation data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight numbers and dates are sent to external aviation APIs, including OpenSky, AeroDataBox/RapidAPI, and optionally AirLabs. <br>
Mitigation: Use the skill only where sharing those lookup details is acceptable, and avoid entering sensitive itinerary information. <br>
Risk: API keys and request URLs may be exposed by local logging or shell history, especially when optional AirLabs requests include a key in the URL. <br>
Mitigation: Use limited API keys, monitor quota, store keys in environment or agent secret storage, and avoid enabling AirLabs in environments that log full URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ImL1s/planefilter) <br>
- [AeroDataBox on RapidAPI](https://rapidapi.com/aedbx-aedbx/api/aerodatabox) <br>
- [AirLabs signup](https://airlabs.co/signup) <br>
- [OpenSky Network API](https://opensky-network.org/api/states/all) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON flight lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and RAPIDAPI_KEY; AIRLABS_KEY is optional for an additional data source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
