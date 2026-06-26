## Description: <br>
Checks OpenClaw documentation and schema before editing OpenClaw configuration files so proposed changes use supported options and types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leon2023happy](https://clawhub.ai/user/leon2023happy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when modifying OpenClaw config files such as openclaw.json or config/*.json. It guides them to check local docs, schema definitions, and OpenClaw documentation before changing configuration values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A proposed OpenClaw configuration change may still be incorrect or incompatible if documentation or schema checks are skipped or stale. <br>
Mitigation: Run the documented local docs and schema checks before editing, consult OpenClaw online documentation when local evidence is missing, and review final config changes before accepting them. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/leon2023happy/openclaw-cfg-safe-edit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration validation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not define executable scripts or require credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
