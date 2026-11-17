## Description:

Helps agents track live aircraft positions by callsign or flight number and list airborne aircraft near a latitude and longitude using the OpenSky Network API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javi23ruiz](https://clawhub.ai/user/javi23ruiz)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams can use this skill to ask an agent where a currently airborne flight is or what aircraft are overhead at specific coordinates. It is suited to live flight lookup tasks where summary text or JSON output is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live flight lookups may send flight numbers or geographic coordinates to a third-party flight-tracking service.

Mitigation: Avoid submitting sensitive or unnecessary locations, and review whether such lookups are acceptable for the deployment environment.

Risk: The skill installs and depends on a third-party PyPI CLI package.

Mitigation: Pin and review the package version before use in stricter environments.

## Reference(s):

- [OpenSky Flight Tracker on ClawHub](https://clawhub.ai/javi23ruiz/skills/opensky-flight-tracker)
- [flight-tracker-cli support issue tracker](https://github.com/javi23ruiz/flight-tracker-cli/issues)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples; CLI output can be human-readable summaries or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI requires the flight-tracker binary, uses no API key, and applies retries and timeout options for OpenSky rate limits.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
