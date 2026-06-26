## Description: <br>
Control smart home devices configured in Smart Plus APP. Use when you need to: (1) Query devices and scenes (lights, AC, switches), (2) Control device power (turn on/off), (3) Control air conditioner (temperature, mode), (4) Trigger smart scenes. Requires MXCHIP_OAUTH_TOKEN environment variable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mxchipyun](https://clawhub.ai/user/mxchipyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent list and control Smart Plus smart-home devices, adjust air conditioners, and trigger configured automation scenes. Because these actions affect real devices, workflows should list targets first and require explicit user confirmation before control operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mxchipyun/mxchip-smart-control) <br>
- [Mxchip Smart Control API Reference](references/api_reference.md) <br>
- [Mxchip MCP Client SDK](scripts/mxchip_mcp_client.py) <br>
- [MXCHIP Official Website](https://www.mxchip.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON-RPC requests and JSON responses, with Markdown guidance, shell snippets, and Python examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MXCHIP_OAUTH_TOKEN. Store the token as a secret and require explicit user confirmation before device control, air-conditioner changes, or scene triggers.] <br>

## Skill Version(s): <br>
1.0.2 (source: skill.json, README.md, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
