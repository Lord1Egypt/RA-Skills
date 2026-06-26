## Description: <br>
Accesses Oura Ring health data through the ouracli command-line tool for sleep, activity, heart rate, readiness, stress, and related metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visionik](https://clawhub.ai/user/visionik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to retrieve Oura Ring health and wellness metrics via shell commands for analysis or reporting. It is suited for scoped queries over sleep, activity, readiness, heart rate, SpO2, stress, workouts, and related Oura data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Oura health data and personal profile output can be sensitive. <br>
Mitigation: Use specific commands and narrow date ranges, and avoid sharing command output unless the user intends to disclose that data. <br>
Risk: The PERSONAL_ACCESS_TOKEN grants access to Oura data if exposed. <br>
Mitigation: Keep the token out of prompts, logs, screenshots, generated reports, and shared repositories. <br>
Risk: The all command can expose every available Oura data type for the requested range. <br>
Mitigation: Prefer a specific data command such as activity, sleep, readiness, heartrate, spo2, or stress unless the user explicitly requests all data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/visionik/ouracli) <br>
- [Oura API documentation](https://cloud.ouraring.com/v2/docs) <br>
- [Oura personal access tokens](https://cloud.ouraring.com/personal-access-tokens) <br>
- [dashdash-spec v0.2.0](https://github.com/visionik/dashdash) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, HTML, Text, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; command output can be JSON, Markdown, HTML, tree text, or dataframe text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Oura Personal Access Token; JSON output is recommended for programmatic analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence, pyproject.toml, CHANGELOG, released 2026-01-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
