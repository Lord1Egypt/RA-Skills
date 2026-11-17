## Description:

Pre-flight environment validator — checks that all required binaries, environment variables, and services are available before running other skills

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check whether local tools, credentials, environment variables, and service connectivity are ready before running stack-specific skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose secrets in logs or saved reports when checking credential environment variables.

Mitigation: Check only whether secrets are set, redact credential values and prefixes, and save reports only after redaction or explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guifav/skills/preflight-check)
- [Docker installation documentation](https://docs.docker.com/get-docker/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON report and human-readable Markdown summary with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill saves a preflight-report.json file and summarizes pass, fail, warning, ready-skill, and blocked-skill results.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence; artifact CHANGELOG.md and claw.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
