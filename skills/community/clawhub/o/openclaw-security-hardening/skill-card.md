## Description: <br>
Protect OpenClaw installations from prompt injection, data exfiltration, malicious skills, and workspace tampering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylejfrost](https://clawhub.ai/user/kylejfrost) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to scan OpenClaw skills, audit outbound data-flow patterns, monitor file integrity, harden workspace configuration, and check new skills before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some commands can persistently change agent rules or modify file permissions outside the workspace. <br>
Mitigation: Run tools without --fix first, review the exact paths reported, and manually approve any permission or rules changes. <br>
Risk: The scanner results are advisory and may miss issues because the bundled scanner has a self-exclusion blind spot. <br>
Mitigation: Treat clean scan results as one input to review rather than proof of safety, and inspect the skill files before installation. <br>
Risk: Adding security rules by appending a template can create broad behavior changes for an agent. <br>
Mitigation: Manually merge the AGENTS.md rules and confirm they match the local workspace policy before use. <br>


## Reference(s): <br>
- [OpenClaw Security Hardening ClawHub Page](https://clawhub.ai/kylejfrost/openclaw-security-hardening) <br>
- [Security Rules Template](assets/security-rules-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and local scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled tools may report findings, modify permissions, append configuration guidance, or create local integrity baselines when invoked with fix or init options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
