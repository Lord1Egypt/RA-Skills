## Description:

Global Weather Service uses Open-Meteo to look up current and forecast weather for global cities and manage scheduled weather subscription pushes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zykkk-power](https://clawhub.ai/user/zykkk-power)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to answer one-time weather questions, generate Chinese weather bulletins, and create or manage scheduled weather pushes for chosen cities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled weather subscriptions can modify persistent delivery jobs in a shared OpenClaw environment without sufficient ownership controls.

Mitigation: Restrict subscription commands to trusted callers, review scheduled jobs before deployment, and add owner checks before allowing updates or deletion.

Risk: Packaged data files include retained subscription and timezone state, including delivery routing identifiers.

Mitigation: Clear packaged data files before deployment and document what subscription data is stored, how long it is retained, and how users can delete it.

Risk: Subscription inputs such as city names and scheduling text can affect generated cron prompts.

Mitigation: Sanitize city and time inputs, validate subscription modes, and scope permissions to Open-Meteo, the two state files, and OpenClaw cron commands.

## Reference(s):

- [Open-Meteo](https://open-meteo.com/)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Global Weather Service on ClawHub](https://clawhub.ai/zykkk-power/skills/global-weather-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown-style weather bulletins, JSON subscription status, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-time reports return direct text; subscription actions can create, update, list, or remove scheduled weather delivery jobs.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
