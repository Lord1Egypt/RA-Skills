## Description:

Kefal Guard monitors OpenClaw hosts for exposed services, privilege escalation paths, unauthorized SSH keys, and novel outbound connections using a manually installed read-only telemetry agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidangularme](https://clawhub.ai/user/davidangularme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use Kefal Guard to check OpenClaw gateways and host environments for exposed services, suspicious access paths, unauthorized SSH keys, and security incidents before or during deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separate Kefal agent can run with elevated access during enrollment and inspect host, process, port, account, and SSH authorized-key fingerprint metadata.

Mitigation: Verify the agent binary independently, prefer least-privilege operation where possible, and request confinement guidance before deployment.

Risk: Host inventory and SSH identity metadata are sent to kefal.dev for dashboard and incident reporting.

Mitigation: Confirm the telemetry schema, retention and deletion controls, tenant isolation terms, and update policy before use on sensitive systems.

Risk: Remediation output may include shell commands that change host configuration if a user runs them.

Mitigation: Review incident details and proposed remediation commands before applying changes.

## Reference(s):

- [Kefal homepage](https://kefal.dev)
- [Kefal installation guide](https://kefal.dev/docs/installation.html)
- [Kefal documentation](https://kefal.dev/docs)
- [ClawHub listing](https://clawhub.ai/davidangularme/skills/kefal-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown security reports with incident summaries, status output, and remediation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a separately installed kefal-agent binary on PATH; the skill itself does not install remote code.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
