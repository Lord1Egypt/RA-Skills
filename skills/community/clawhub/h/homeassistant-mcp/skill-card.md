## Description: <br>
Provides structured access to Home Assistant devices, sensors, and cameras via MCP, with documented handling for camera snapshots, garage doors, and device control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsnkzdeny](https://clawhub.ai/user/dsnkzdeny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home operators use this skill to connect an agent to their own Home Assistant environment for device, sensor, camera, and garage-door workflows. It is intended for environments where the user controls the Home Assistant endpoint and can manage access tokens safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A long-lived Home Assistant token can expose sensitive smart-home state, device controls, and camera data. <br>
Mitigation: Install only for a Home Assistant endpoint you control, use the least-privileged token available, and rotate or revoke tokens that are no longer needed. <br>
Risk: Shell-based REST fallbacks can retrieve camera snapshots or entity state outside normal MCP tool boundaries. <br>
Mitigation: Prefer MCP tools when they work, require explicit confirmation before camera or garage actions, and delete saved snapshots when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/dsnkzdeny/homeassistant-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference MCP tools, REST API fallbacks, and local media files; requires a user-supplied Home Assistant endpoint and access token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
