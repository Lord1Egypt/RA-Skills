## Description: <br>
Mini-HIDS monitors Linux auth and web logs, scans web roots for suspicious webshell patterns, tracks local blacklist state, and exposes MCP tools for agent-assisted host intrusion response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netkr](https://clawhub.ai/user/netkr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill to inspect and operate a lightweight Linux host intrusion detection workflow on a small server, including status checks, recent alerts, blacklist review, manual ban/unban actions, and webshell scans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Firewall ban and unban actions can accidentally block legitimate users or the operator. <br>
Mitigation: Review TRUSTED_IPS, BAN_TIME, log paths, web roots, and FIREWALL_BACKEND before use, and restrict MCP access to trusted local agents or operators. <br>
Risk: The daemon and MCP workflow require privileged local access to logs and firewall controls on the target Linux host. <br>
Mitigation: Install only on hosts where this level of local security control is intended, and avoid exposing the MCP server beyond the local trusted integration. <br>
Risk: Regex-based detection and webshell scanning can produce false positives or miss attacks. <br>
Mitigation: Treat alerts as signals for review, tune thresholds and trusted IPs for the host, and confirm findings before broad operational action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netkr/skills/mini-hids) <br>
- [Mini-HIDS documentation](artifact/SKILL.md) <br>
- [LLM project map](artifact/llms.txt) <br>
- [Runtime configuration](artifact/config.json) <br>
- [MCP client configuration example](artifact/examples/claude_desktop_mcp.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or concise natural-language guidance with shell commands and structured JSON MCP tool results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP tool results include structuredContent for status, alerts, blacklist entries, ban/unban outcomes, and webshell scan summaries.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
