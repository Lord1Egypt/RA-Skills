## Description: <br>
Inspect and operate a local Mihomo/Clash.Meta/Clash Verge/ClashMac instance through its REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkgogogo](https://clawhub.ai/user/parkgogogo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local Mihomo or Clash-compatible proxy status, list nodes and groups, check latency, inspect connections, and perform deliberate control actions such as switching routes, flushing cache, or restarting the proxy service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a local controller secret and read Mihomo or Clash configuration paths. <br>
Mitigation: Install only when this local access is acceptable, and begin with read-only commands before allowing control operations. <br>
Risk: Switching proxy groups, flushing caches, or restarting Mihomo can change routing behavior, drop connections, or disrupt the proxy service. <br>
Mitigation: Treat switch, flush, restart, and raw API actions as deliberate changes and confirm that service disruption or routing changes are acceptable before running them. <br>


## Reference(s): <br>
- [Mihomo API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local REST API calls through the bundled shell helper when the agent executes commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
