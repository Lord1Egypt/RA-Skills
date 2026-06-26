## Description: <br>
OpenClaw Memory Kit helps agents scaffold, sanitize, and share an OpenClaw multi-agent memory workspace with reusable configuration, role prompts, task-board conventions, and startup commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sora-mury](https://clawhub.ai/user/sora-mury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to package an existing OpenClaw memory setup for teammates, remove private details from a live configuration, or bootstrap a fresh memory-focused OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent memory workspace can accumulate sensitive information in generated memory and task files. <br>
Mitigation: Use an isolated target directory, keep real tokens and .env files out of shared kits, and periodically inspect or delete generated memory and task files. <br>
Risk: Bootstrapping or adapting a live setup can accidentally carry private paths, app IDs, channel bindings, or personal scope names into a shared kit. <br>
Mitigation: Replace private values with placeholders, target-root-relative paths, generic role IDs, and loopback endpoints before sharing. <br>
Risk: Startup or bootstrap commands may change the local OpenClaw state if pointed at an existing directory. <br>
Mitigation: Default to a separate target root, review bootstrap scripts before running them, and use overwrite flags only when explicitly intended. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [Generated Files](references/generated-files.md) <br>
- [Sanitization Rules](references/sanitization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell commands, configuration descriptions, and generated workspace file expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve placeholders for secrets and use isolated target directories for generated memory workspaces.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
