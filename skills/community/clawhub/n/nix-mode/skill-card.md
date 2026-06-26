## Description: <br>
Handle Clawdbot operations in Nix mode (configuration management, environment detection). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chronicuser21](https://clawhub.ai/user/Chronicuser21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to help Clawdbot recognize Nix-managed environments, respect immutable installation paths, and give appropriate configuration and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may give unsuitable dependency or setup advice if a user's Nix-mode environment variables or paths differ from the expected setup. <br>
Mitigation: Confirm that CLAWDBOT_NIX_MODE and the relevant configuration and state paths match the local Nix-managed environment before applying guidance. <br>
Risk: Auto-install or self-modification suggestions can conflict with immutable Nix-managed installations. <br>
Mitigation: Use Nix package management for dependency changes and avoid agent-directed auto-install flows in Nix mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Chronicuser21/nix-mode) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions] <br>
**Output Format:** [Markdown or plain text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no automatic installation steps are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
