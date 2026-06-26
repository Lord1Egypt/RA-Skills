## Description: <br>
Aircraft tracking and aviation weather through Pilot Protocol service agents for ADS-B feeds, airport directory data, METAR, TAF, AIRMET, and SIGMET queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and operators use this skill to discover and query flight-related Pilot Protocol service agents for live aircraft positions, aircraft records, airport metadata, and aviation weather reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Pilot Protocol, the pilotctl binary, and joining network 9 for external aviation data access. <br>
Mitigation: Install and run it only with a trusted pilotctl binary, a trusted Pilot Protocol daemon, and the intended network configuration. <br>
Risk: Aviation queries and inbox reads pass through an external overlay, and summary or free-text responses may involve Gemini. <br>
Mitigation: Avoid sending sensitive operational data unless the external services and data handling path are approved for the use case. <br>
Risk: ADS-B coverage can be incomplete and the skill does not provide proprietary radar or military-restricted feeds. <br>
Mitigation: Treat outputs as operational data aids and verify critical aviation decisions against authoritative sources. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-flights) <br>
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses may include structured JSON data, plain text help, and Gemini-generated summaries returned through pilotctl inbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
