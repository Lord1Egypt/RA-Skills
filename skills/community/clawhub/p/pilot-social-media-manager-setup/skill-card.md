## Description:

Deploys a three-agent social media management setup where planner, creator, and analyst agents coordinate content planning, post creation, and performance feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators setting up Pilot Protocol or OpenClaw social media workflows use this skill to configure three cooperating agents for content planning, post creation, engagement tracking, and feedback loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup changes Pilot agent configuration and writes a persistent manifest under ~/.pilot/setups.

Mitigation: Review the selected role, hostname prefix, and generated manifest before applying changes in a production or brand-owned environment.

Risk: The setup establishes persistent trust paths between peer agents through handshakes.

Mitigation: Verify each peer agent out of band before handshakes and inspect the trust state after setup.

Risk: The setup installs companion skills that may change over time.

Mitigation: Pin and verify companion skill versions before installation.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-social-media-manager-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, related Pilot Protocol skills, and a running daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
