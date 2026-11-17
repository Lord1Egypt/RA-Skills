## Description:

Weather forecasts and historical climate via Pilot Protocol service agents for Open-Meteo forecast, archive, air quality, marine, flood, and Seven Timer astronomy data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to discover Pilot Protocol weather agents, inspect each agent's filter contract, and request current, forecast, historical, marine, flood, air-quality, sunrise/sunset, or astronomy weather data by coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather requests are sent to Pilot Protocol service agents over the configured overlay network.

Mitigation: Install only when that network posture is acceptable, keep the daemon configuration under operator control, and verify target agent contracts with /help before sending requests.

Risk: Free-text summary requests may include sensitive locations or private context and can be processed by remote agents or a Gemini-backed summarizer.

Mitigation: Prefer structured /data requests for sensitive workflows and avoid placing private context in /summary or free-text prompts.

Risk: The weather catalog can change and individual service-agent schemas may differ from the documented snapshot.

Mitigation: Run a fresh list-agents query and read the selected agent's /help output before relying on filters in automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-weather)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for querying remote Pilot Protocol agents; structured data responses are retrieved through pilotctl inbox.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
