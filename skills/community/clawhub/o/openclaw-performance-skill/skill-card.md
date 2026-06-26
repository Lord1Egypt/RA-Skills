## Description: <br>
Provides OpenClaw performance diagnostics, configuration optimization, prompt guidance, and monitoring utilities for improving response time, memory use, token consumption, and context retention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ynxiyan](https://clawhub.ai/user/ynxiyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose OpenClaw performance issues, apply optimization configuration, generate optimized prompt guidance, and monitor runtime behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optimization scripts can read local OpenClaw configuration and persistently change ~/.openclaw/config.json. <br>
Mitigation: Review the scripts and configuration changes before running them, keep a backup of existing OpenClaw configuration, and restore from backup if behavior changes unexpectedly. <br>
Risk: Diagnostic reports and monitoring logs may capture local configuration, system details, or operational information. <br>
Mitigation: Run the skill only in workspaces where such reports are acceptable, review generated reports before sharing them, and remove sensitive details. <br>
Risk: Automatic optimization can change performance, context retention, model selection, and prompt behavior in ways that may affect output quality. <br>
Mitigation: Apply changes gradually, test behavior after each change, and monitor quality and performance before using the optimized setup for important workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ynxiyan/openclaw-performance-skill) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw performance documentation](https://docs.openclaw.ai/performance) <br>
- [OpenClaw context management documentation](https://docs.openclaw.ai/context-management) <br>
- [OpenClaw tools documentation](https://docs.openclaw.ai/tools) <br>
- [OpenClaw community discussions](https://github.com/openclaw/openclaw/discussions) <br>
- [OpenClaw issues](https://github.com/openclaw/openclaw/issues) <br>
- [Bilibili performance tutorial](https://www.bilibili.com/video/BV1CDAVziEwQ) <br>
- [Optimization guide](docs/OPTIMIZATION-GUIDE.md) <br>
- [Optimized configuration template](configs/optimized-config.json) <br>
- [Optimized prompt](prompts/optimized-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JavaScript scripts, JSON configuration, shell commands, and diagnostic reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scripts that can read OpenClaw configuration, write optimized configuration, create backups, generate prompts, and write local logs or reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
