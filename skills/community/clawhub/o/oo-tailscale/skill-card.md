## Description:

Use an OOMOL-connected Tailscale account to inspect and manage tailnet users, devices, keys, DNS, policies, services, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Tailnet administrators and operators use this skill to inspect and manage Tailscale resources through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook-secret rotation and other state changes can alter tailnet configuration or disrupt integrations.

Mitigation: Require explicit user approval for each state-changing action and its exact payload.

Risk: The CLI installer is unverified and may affect other installed agent skills.

Mitigation: Verify the installer before running it and review its effects on installed skills.

Risk: Connector actions can return secrets or expose sensitive tailnet information.

Mitigation: Connect only the required Tailscale permissions and protect any returned secrets.

## Reference(s):

- [Tailscale](https://tailscale.com)
- [Tailscale API documentation](https://tailscale.com/docs/reference/tailscale-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-tailscale)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Natural language guidance, JSON action payloads, and connector response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the live connector schema; output depends on the selected Tailscale action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
