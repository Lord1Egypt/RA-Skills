## Description: <br>
Connect an MCP-compatible agent to local Oura readiness, sleep, activity, HRV, heart-rate, SpO2, and workout data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users of MCP-compatible clients use this skill to install, configure, troubleshoot, and apply privacy boundaries for an Oura MCP connector that exposes local readiness, sleep, activity, HRV, heart-rate, SpO2, and workout data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector can expose sensitive health and profile data such as sleep, heart-rate, HRV, SpO2, activity, workouts, and personal profile information. <br>
Mitigation: Treat Oura data as private health information, keep user consent explicit, and avoid printing private data or credentials. <br>
Risk: OAuth tokens and local connector files may be mishandled by the agent or MCP client. <br>
Mitigation: Keep files under ~/.oura-mcp/ private, do not print OAuth tokens or local token files, and revoke Oura access when the connector is no longer needed. <br>
Risk: The workflow depends on a referenced npm package and the MCP client that receives Oura data. <br>
Mitigation: Install only when the npm package and receiving MCP client are trusted, and prefer connection_status, manifest, doctor, privacy_audit, or dry-run checks before live provider calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidmosiah/oura-mcp) <br>
- [Oura MCP docs/site](https://wellness.delx.ai/connectors/oura) <br>
- [Repository named by skill artifact](https://github.com/davidmosiah/ouramcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes privacy and safety guidance for OAuth tokens and health-related Oura data.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
