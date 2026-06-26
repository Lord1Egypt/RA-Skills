## Description: <br>
Securely migrate OpenClaw Agent configuration, memory, and skills to a new machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenjie2024](https://clawhub.ai/user/wenjie2024) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to export encrypted archives of agent configuration, memory, skills, and related state, then import them on another machine while normalizing local workspace paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration archives can contain sensitive agent state, including configuration, memory, skills, and credentials. <br>
Mitigation: Use a strong password, keep archives private, and treat exported .oca files like sensitive backups. <br>
Risk: Importing an untrusted archive can alter destination OpenClaw state and influence future agent behavior. <br>
Mitigation: Import only archives you created or fully trust, and back up the destination OpenClaw state before restoring. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/wenjie2024/openclaw-migrator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with command examples; the CLI produces encrypted .oca archive files during export and restored local configuration during import.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses password-protected local migration archives for OpenClaw agent state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
