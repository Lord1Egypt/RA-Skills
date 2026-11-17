## Description:

Authenticate with LiberFi to register accounts, log in, manage session state, and verify wallet assignments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombmod](https://clawhub.ai/user/bombmod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to authenticate agents or human users with LiberFi, inspect authentication state, and manage local session credentials for LiberFi workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to install a global npm CLI without asking and to hide package-installation failures.

Mitigation: Require explicit approval before any global install, pin and verify the @liberfi.io/cli package, and report installation failures accurately.

Risk: Authentication creates persistent local key and session files containing key material, wallet addresses, and a JWT.

Mitigation: Treat ~/.liberfi/session.json and ~/.liberfi/keys/*.json as sensitive credentials, keep restrictive file permissions, and never log, display, or transmit their contents.

## Reference(s):

- [LiberFi homepage](https://liberfi.io)
- [ClawHub skill page](https://clawhub.ai/bombmod/skills/liberfi-auth)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the LiberFi CLI and creates local session and key files under ~/.liberfi.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
