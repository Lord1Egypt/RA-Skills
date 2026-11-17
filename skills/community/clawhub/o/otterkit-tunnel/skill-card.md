## Description:

OtterKit Tunnel helps agents expose local services through public HTTPS tunnels, create capture-only webhook endpoints, and replay deliveries for debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shivamanupadi](https://clawhub.ai/user/shivamanupadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need a public URL for a local service, OpenClaw webhook gateway, or webhook test endpoint, including capture, forwarding, inspection, and replay workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose selected local services to the public internet.

Mitigation: Expose only intended services, keep gateway and hooks tokens enabled, use HTTP Basic auth where appropriate, and stop tunnels when public access is no longer needed.

Risk: Persistent endpoints can remain available longer than intended.

Mitigation: Prefer short TTLs and avoid ttl never unless a long-lived endpoint is explicitly required.

Risk: The workflow may execute an unpinned npm package.

Mitigation: Install only if OtterKit is trusted and use a pinned or preinstalled OtterKit version where possible.

Risk: Secrets can be exposed through command-line arguments or forwarded request handling.

Mitigation: Avoid putting real secrets directly in command-line arguments and use dedicated webhook tokens or environment-based credentials.

## Reference(s):

- [OtterKit Documentation](https://www.otterkit.com/docs)
- [ClawHub Skill Page](https://clawhub.ai/shivamanupadi/skills/otterkit-tunnel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-output command variants for scripting.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
