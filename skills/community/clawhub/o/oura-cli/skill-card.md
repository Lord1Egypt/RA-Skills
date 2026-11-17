## Description:

Retrieve Oura Ring health and biometric data through a local CLI for sleep, activity, readiness, heart rate, workouts, and related wellness categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supadoopa](https://clawhub.ai/user/supadoopa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to authenticate a local Oura CLI and retrieve JSON health data that an agent can parse into user-facing answers. It is suited to personal biometric queries such as sleep, readiness, activity, heart rate, and device status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local OAuth credentials and tokens can grant access to sensitive Oura health data if the config file is exposed.

Mitigation: Restrict permissions on ~/.config/oura-cli and config.json, avoid shared machines, and revoke tokens after testing or when access is no longer needed.

Risk: CLI output may expose health, profile, and device data in terminal logs, transcripts, or shell history.

Mitigation: Run commands only in trusted sessions and avoid storing or sharing raw command output unless the user has approved it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/supadoopa/skills/oura-cli)
- [Oura Developer Portal](https://cloud.ouraring.com/oauth/developer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI returns JSON from Oura API responses; agent responses should summarize that data in natural language.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
