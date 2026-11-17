## Description:

Manage a Tailscale tailnet from chat by checking status, listing devices, pinging hosts, running network diagnostics, and checking serve/funnel configuration with best-effort public IP masking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lookupmark](https://clawhub.ai/user/lookupmark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and tailnet administrators use this skill to inspect Tailscale device status and connectivity from an agent chat while avoiding write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal Tailscale device, hostname, owner/whois, status, and diagnostic information from the current tailnet.

Mitigation: Install only in environments where agent access to tailnet inventory and diagnostics is acceptable.

Risk: Public IP masking is best-effort and the security evidence notes incomplete redaction paths.

Mitigation: Review output before sharing it externally and avoid relying on masking as a privacy boundary.

Risk: Broad conversational triggers may activate the skill when a user intended only a general network discussion.

Mitigation: Prefer explicit Tailscale command requests and review trigger behavior before deployment.

## Reference(s):

- [Tailscale CLI documentation](https://tailscale.com/kb/1080/cli)
- [ClawHub skill page](https://clawhub.ai/lookupmark/skills/lookupmark-tailscale-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured JSON with shell command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Tailscale device, hostname, owner/whois, status, and diagnostic information; public IP masking is best-effort.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
