## Description:

Browser automation patterns for OpenClaw: multi-step flows, login checks, tab management, stale ref recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronmda](https://clawhub.ai/user/aaronmda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run multi-step OpenClaw browser flows with clearer tab management, login-state checks, stale reference recovery, and blocker reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using an existing browser profile can interact with sites where the user is already signed in.

Mitigation: Review browser actions before allowing sensitive account changes, and stop for login, 2FA, captcha, permissions, or other manual blockers.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json]

**Output Format:** [Markdown guidance with inline shell commands and JSON browser tool examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers browser state checks, stable tab handles, snapshot-before-action workflows, stale reference recovery, existing user browser sessions, and Google Meet flows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
