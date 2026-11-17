## Description:

Inspect and operate a local Mihomo/Clash.Meta/Clash Verge/ClashMac instance through its REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkgogogo](https://clawhub.ai/user/parkgogogo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local Mihomo-compatible proxy status, list nodes and groups, review latency and connections, and make explicit route, cache, restart, or API-control changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a local Mihomo bearer secret and send it over plaintext HTTP to a configurable controller host.

Mitigation: Keep the controller bound to localhost where possible, avoid passing secrets on the command line, and review controller host settings before use.

Risk: Switch, flush, restart, and raw API calls can change proxy routing or network state.

Mitigation: Use read-only commands first and run state-changing commands only after the user explicitly asks for that change.

## Reference(s):

- [Mihomo API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers read-only status, proxy, group, and connection checks before proposing state-changing operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
