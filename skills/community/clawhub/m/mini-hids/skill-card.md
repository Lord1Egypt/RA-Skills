## Description:

Real-time Linux log monitoring and AI-assisted detection of brute force attacks, web attacks, and webshells with automated IP blocking and whitelist support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netkr](https://clawhub.ai/user/netkr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Mini-HIDS to give an agent local visibility into SSH and web attack signals on small Linux servers, inspect alerts and blacklist state, and trigger explicit ban or unban actions through MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic bans can change firewall state based on log data that may be ambiguous or spoofable.

Mitigation: Review the server configuration before installation, pin trusted IPs and monitored paths narrowly, and avoid automatic web-log bans behind proxies unless client identity is trustworthy.

Risk: The MCP server can trigger ban and unban operations and acts as a privileged local control plane.

Mitigation: Expose MCP only to trusted local clients and run it with the least privileges compatible with the selected firewall backend.

Risk: Regex-based detections can produce false positives or miss higher-fidelity attack patterns.

Mitigation: Treat alerts and webshell matches as triage signals and review the relevant logs or files before relying on them for irreversible response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netkr/skills/mini-hids)
- [Publisher profile](https://clawhub.ai/user/netkr)
- [Mini-HIDS documentation](artifact/SKILL.md)
- [LLM project map](artifact/llms.txt)
- [MCP client configuration example](artifact/examples/claude_desktop_mcp.json)

## Skill Output:

**Output Type(s):** [JSON, text, configuration, guidance]

**Output Format:** [Structured JSON tool responses with concise operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tool calls can inspect status, alerts, and blacklist state, scan web roots, and request firewall ban or unban actions.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
