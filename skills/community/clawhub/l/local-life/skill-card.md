## Description:

Local Life provides a Portuguese local-day dashboard with current weather, air quality, exchange rates, holidays, moon phase, and contextual tips for a selected city.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pedrohenrique202525](https://clawhub.ai/user/pedrohenrique202525)

### License/Terms of Use:


## Use Case:

Users and agents use this skill to assemble a concise local status dashboard for a chosen city, defaulting to Goiânia when no city is supplied. It is intended for everyday local context such as weather, UV, currency rates, national holidays, moon phase, air quality, and simple daily recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested or default city can be sent to third-party weather, currency, holiday, and search services.

Mitigation: Specify only the city needed for the request and name the intended city explicitly if the Goiânia default is not appropriate.

Risk: Real-time public API and search results can be unavailable, stale, or inconsistent across providers.

Mitigation: Treat the dashboard as a convenience summary and verify critical weather, air-quality, holiday, or market information with authoritative sources before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pedrohenrique202525/skills/local-life)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown containing a formatted plain-text dashboard in a code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portuguese output with translated weather and moon-phase labels; uses Goiânia as the default city when none is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
