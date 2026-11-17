## Description:

Retrieves and summarizes Oura Ring health, sleep, activity, readiness, and biometric data through a command-line interface for the Oura API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruhrpotter](https://clawhub.ai/user/ruhrpotter)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query an authenticated local Oura CLI for sleep, readiness, activity, physiological, and profile data, then summarize the returned JSON for personal health questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Oura OAuth credentials and sensitive health or biometric data.

Mitigation: Protect the local token file with restrictive permissions, avoid sharing terminal output that contains health data or secrets, and revoke or rotate OAuth credentials if exposure is suspected.

Risk: The installation flow asks users to build and run unpinned third-party code.

Mitigation: Install only from a pinned, reviewed release or commit of the upstream repository and review the code before granting access to Oura data.

## Reference(s):

- [Oura Ring Integration on ClawHub](https://clawhub.ai/ruhrpotter/skills/oura)
- [ruhrpotter ClawHub Profile](https://clawhub.ai/user/ruhrpotter)
- [Oura CLI Repository](https://github.com/ruhrpotter/oura-cli)
- [Oura Developer Portal](https://cloud.ouraring.com/oauth/developer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and natural-language summaries of CLI JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated local Oura CLI and date ranges resolved to YYYY-MM-DD.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
