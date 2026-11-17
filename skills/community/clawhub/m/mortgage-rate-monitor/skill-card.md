## Description:

Published as Mortgage Rate Monitor, this release's artifact contents provide a concise OpenClaw weather briefing prompt rather than mortgage-rate monitoring behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-chi](https://clawhub.ai/user/li-chi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the published skill as a prompt package for generating short spoken weather briefings from city, unit system, and optional audience inputs. Confirm the intended release before relying on it for mortgage-rate monitoring because the server metadata and packaged artifact behavior disagree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release metadata and artifact content disagree: server metadata names Mortgage Rate Monitor, while packaged files describe weather-brief behavior.

Mitigation: Confirm the intended package before relying on the skill for mortgage-rate monitoring; treat the current artifacts as a weather briefing prompt until the publisher republishes matching content.

Risk: Weather forecasts can be inaccurate or stale without a trusted live weather data source.

Mitigation: Use a trusted weather data source when factual forecasts matter and review generated briefings before scheduled or user-facing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li-chi/skills/mortgage-rate-monitor)
- [Artifact README](artifact/README.md)
- [Artifact manifest](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text weather briefing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can tailor a practical recommendation when an audience is provided.]

## Skill Version(s):

1.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
