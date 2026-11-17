## Description:

Nirvana is a local-first OpenClaw inference plugin that routes queries to Ollama by default, optionally falls back to cloud models, and audits privacy boundary decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shivaclaw](https://clawhub.ai/user/shivaclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Nirvana to run OpenClaw model inference locally where possible, protect private agent context before any cloud fallback, and monitor routing, audit, and performance signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious by ClawHub security evidence for broad privacy promises, cloud-routing controls, permissions, and Docker guidance that are inconsistent for automatic installation.

Mitigation: Review before installing in sensitive OpenClaw environments and verify that the deployed configuration matches the intended local-only or cloud-fallback posture.

Risk: Cloud fallback can send sanitized prompts to configured cloud providers if local inference is unavailable or the router chooses a cloud model.

Mitigation: Use local-only settings for sensitive workloads, confirm cloud routing is disabled when required, and avoid entering secrets unless no cloud provider can be invoked.

Risk: Docker guidance and service exposure may create unnecessary network or credential exposure.

Mitigation: Bind Docker services to localhost, replace fixed credentials, and pin images or releases before production use.

Risk: Manifest permissions include access to identity, memory, session, Docker, and Ollama resources.

Mitigation: Narrow permissions to plugin-owned files and the minimum Ollama API access needed for the deployment.

## Reference(s):

- [Nirvana ClawHub Skill Page](https://clawhub.ai/shivaclaw/skills/nirvana-plugin)
- [README](artifact/README.md)
- [Installation Guide](artifact/INSTALL.md)
- [Plugin Manifest](artifact/plugin-manifest.json)
- [Configuration Schema](artifact/config.schema.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Model responses with JSON routing metadata, audit logs, metrics, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be served by local Ollama or configured cloud fallback; privacy stripping and audit behavior depend on deployment configuration.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence and plugin-manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
