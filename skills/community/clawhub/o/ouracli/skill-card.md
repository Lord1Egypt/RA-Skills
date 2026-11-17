## Description:

Access Oura Ring health data through the ouracli CLI, including sleep, activity, heart rate, readiness, stress, SpO2, workout, and profile data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visionik](https://clawhub.ai/user/visionik)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to retrieve and analyze their Oura Ring health metrics with Bash commands. It is most useful when the agent needs reliable JSON output for sleep, activity, readiness, heart rate, stress, SpO2, workout, session, tag, rest-mode, or profile data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve broad Oura health and profile data, including sensitive sleep, activity, heart rate, stress, SpO2, and personal information.

Mitigation: Let an agent access the Oura token only when needed, avoid broad all-data requests unless requested, and treat tokens and outputs as sensitive health data.

Risk: Generated HTML reports may expose private health data and have script-execution or CDN-related risk.

Mitigation: Prefer JSON for analysis, and avoid opening or sharing generated HTML reports until the HTML escaping and CDN concerns are fixed.

Risk: Some health fields can be misread, such as readiness contributor scores being mistaken for direct heart rate measurements.

Mitigation: Use the documented field meanings and avoid interpreting readiness contributor scores as BPM; use heartrate output for actual heart rate values.

## Reference(s):

- [Oura API v2 Documentation](https://cloud.ouraring.com/v2/docs)
- [Oura Personal Access Tokens](https://cloud.ouraring.com/personal-access-tokens)
- [dashdash-spec v0.2.0](https://github.com/visionik/dashdash)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, HTML, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and optional CLI output in JSON, Markdown, HTML, tree, or dataframe formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PERSONAL_ACCESS_TOKEN and may process sensitive health and profile data.]

## Skill Version(s):

0.1.0 (source: evidence release, pyproject.toml, CHANGELOG released 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
