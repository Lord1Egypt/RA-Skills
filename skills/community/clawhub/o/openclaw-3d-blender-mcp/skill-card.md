## Description:

Installs and configures Blender MCP for OpenClaw, including local and remote setup, ngrok guidance, verification scripts, troubleshooting, and prerequisite resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejay7](https://clawhub.ai/user/yejay7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up Blender MCP, verify a Blender connection, inspect scenes, and troubleshoot common 3D creation issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded public ngrok endpoints may route Blender MCP traffic to an unintended remote host.

Mitigation: Prefer `localhost:9876` for local use and remove or replace hard-coded ngrok hosts before running scripts.

Risk: Unauthenticated remote Blender MCP access can allow remote control of a Blender session.

Mitigation: Do not expose Blender MCP over public ngrok without authentication and encrypted transport.

Risk: Helper scripts launch `blender-mcp` through `uvx`, which may fetch or run an unreviewed package version.

Mitigation: Pin `blender-mcp` to a reviewed version and pass only the minimum required environment variables to subprocesses.

## Reference(s):

- [Openclaw 3d Blender MCP on ClawHub](https://clawhub.ai/yejay7/skills/openclaw-3d-blender-mcp)
- [blender-mcp Official Repo](https://github.com/ahujasid/blender-mcp)
- [blender-orchestrator](https://github.com/mlolson/blender-orchestrator)
- [I Made Claude Use Blender](https://www.youtube.com/watch?v=dxlyCPGCvy8)
- [Sistema de Coordenadas en Blender](references/coordinate_system.md)
- [Errores Comunes en Blender MCP - Soluciones](references/common_errors.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes helper scripts for Blender MCP connection verification and scene inspection.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/_meta.json, skill footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
