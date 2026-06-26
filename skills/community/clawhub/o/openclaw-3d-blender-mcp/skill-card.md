## Description: <br>
Instalación completa de Blender MCP para OpenClaw. Incluye setup local/remoto, ngrok, verificación, troubleshooting y estudio de 3 recursos obligatorios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejay7](https://clawhub.ai/user/yejay7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to configure Blender MCP for OpenClaw, verify local or remote Blender connectivity, inspect scenes, and troubleshoot common setup and coordinate-system issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can default to hard-coded public ngrok endpoints. <br>
Mitigation: Prefer localhost-only setup and replace or remove hard-coded ngrok hosts before running scripts. <br>
Risk: Direct remote client scripts can send Blender commands or Python code without clear user control. <br>
Mitigation: Run remote client scripts only against endpoints you own and trust, and review commands before execution. <br>
Risk: The execute_blender_code path provides full Blender Python execution. <br>
Mitigation: Treat Blender Python execution as privileged: review code first and limit Blender access to trusted projects and files. <br>


## Reference(s): <br>
- [Blender MCP official repository](https://github.com/ahujasid/blender-mcp) <br>
- [Blender Orchestrator repository](https://github.com/mlolson/blender-orchestrator) <br>
- [I Made Claude Use Blender](https://www.youtube.com/watch?v=dxlyCPGCvy8) <br>
- [Sistema de Coordenadas en Blender](references/coordinate_system.md) <br>
- [Errores Comunes en Blender MCP - Soluciones](references/common_errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, verification commands, troubleshooting guidance, and helper scripts for Blender MCP workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
