## Description: <br>
Installation and setup guide for Tesla vehicle control and telemetry via the tescmd node. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Oceanswave](https://clawhub.ai/user/Oceanswave) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and pair the tescmd node so agents can access Tesla vehicle control, telemetry, and Gateway integrations after user-led authentication and pairing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-connected Tesla vehicle access can expose sensitive vehicle control and telemetry capabilities to the agent environment. <br>
Mitigation: Install only for trusted agents and gateways, review the runtime tescmd tools before allowing access, keep the node stopped when not needed, and revoke stored tokens when access should end. <br>
Risk: Persistent Tesla and OpenClaw credentials are stored locally and may be exposed by loose file permissions or command-line token usage. <br>
Mitigation: Protect files under ~/.config/tescmd with restrictive permissions, prefer OAuth and pairing flows over command-line tokens, and avoid sharing configuration files. <br>
Risk: The setup flow references a remote installer pattern for Tailscale. <br>
Mitigation: Prefer official signed install channels and review installation commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Oceanswave/openclaw-tescmd) <br>
- [openclaw-tescmd plugin repository](https://github.com/oceanswave/openclaw-tescmd) <br>
- [tescmd node repository](https://github.com/oceanswave/tescmd) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes interactive setup checkpoints and security-sensitive credential handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 0.9.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
