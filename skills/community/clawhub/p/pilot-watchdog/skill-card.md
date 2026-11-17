## Description:

Security monitoring for suspicious network patterns in Pilot Protocol networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor Pilot Protocol networks for suspicious connection patterns, security anomalies, trust relationship changes, and score drops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the shell workflow handles daemon data unsafely enough to require review before installation.

Mitigation: Review and harden the Bash snippets before use, including validation of score fields as bounded integers.

Risk: The watchdog writes state and alert files under the Pilot daemon data path.

Mitigation: Protect the watchdog state directory with owner-only permissions and run the continuous loop only under an account whose files and environment may be exposed to that daemon data path.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-watchdog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Bash snippets and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces monitoring setup commands, alerting examples, and operational guidance for use with pilotctl and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
