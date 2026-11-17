## Description:

Deploy a recruitment pipeline with 3 agents for candidate sourcing, screening, and interview scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hiring operations teams use this skill to configure a three-agent recruitment workflow for candidate sourcing, resume screening, and interview scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses broad shell-based installation and configuration steps with mutable third-party skill installs.

Mitigation: Review commands before execution, use approved and pinned dependency skills, and run setup only in an authorized hiring environment.

Risk: The workflow can move candidate profile, screening, Slack, calendar, and webhook data between agents and external services.

Mitigation: Confirm what applicant data may be shared, restrict destinations to approved peers and services, and verify peer identities before handshakes.

Risk: Hostname prefixes and peer names are user-supplied.

Mitigation: Restrict prefixes to safe hostname characters before applying hostnames or initiating handshakes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-recruitment-pipeline-setup)
- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl, clawhub, role-specific skills, and a running daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
