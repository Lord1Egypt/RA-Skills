## Description: <br>
Cryptographic verification for installed skills that signs skill directories with SHA-256 hashes and later verifies whether files were modified, added, or removed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to create and check local trust manifests for installed Agent Skills, identifying tampering or unsigned skills in OpenClaw-compatible workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can move, quarantine, delete, or restore installed skills in the selected workspace. <br>
Mitigation: Use sign, verify, list, and status for routine checks; make backups before using reject, quarantine, restore, or protect. <br>
Risk: Running against the wrong workspace can alter unintended skill directories. <br>
Mitigation: Pass only the intended OpenClaw workspace path and review the resolved workspace before using commands that change files. <br>


## Reference(s): <br>
- [Openclaw Signet on ClawHub](https://clawhub.ai/AtlasPA/openclaw-signet) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON manifest files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local trust manifests, snapshots, and quarantine evidence under the selected workspace when commands request those actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
