## Description:

Access your AI agent's web UI from anywhere and share it securely -- automatic HTTPS, SSO access control, no VPN or port forwarding needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jspanos](https://clawhub.ai/user/jspanos)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to expose an agent Control UI or other managed local service through HLE with HTTPS and access controls for remote access or collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make selected local services reachable from the internet, including sensitive agent or admin interfaces.

Mitigation: Expose only intended services, avoid publishing admin tools without strong native authentication, and review active tunnels regularly.

Risk: Weak or missing access controls could allow unintended access to exposed services.

Mitigation: Prefer SSO allow lists, avoid auth-none for sensitive services, and use temporary share links or other access controls deliberately.

Risk: Persistent background tunnels can remain active longer than intended.

Mitigation: Use persistent process managers only when the operator knows how to stop and remove the tunnel.

Risk: The HLE API key grants tunnel management access if exposed.

Mitigation: Protect the API key and avoid placing it in shared logs, public files, or broadly readable service definitions.

## Reference(s):

- [HLE OpenClaw integration docs](https://hle.world/docs/integrations/openclaw)
- [HLE website](https://hle.world)
- [HLE Tunnel examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/jspanos/skills/hle-tunnel)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for the HLE CLI, Docker, Docker Compose, access controls, and tunnel management.]

## Skill Version(s):

1.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
