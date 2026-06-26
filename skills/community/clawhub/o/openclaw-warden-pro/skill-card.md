## Description: <br>
OpenClaw Warden Pro is a local workspace security skill that detects unauthorized modifications and prompt injection patterns, then can respond with snapshot restore, skill quarantine, git rollback, and protection sweeps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent workspace operators use this skill to baseline and monitor local agent workspaces, inspect prompt-injection or integrity findings, and optionally run countermeasures that restore files or quarantine suspicious skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic protection can restore workspace files or quarantine skills without a confirmation step. <br>
Mitigation: Establish and inspect the baseline first, run scan, verify, or full manually, and enable protect only after expected findings and false positives are understood. <br>
Risk: Startup or heartbeat automation can apply countermeasures during normal agent sessions. <br>
Mitigation: Avoid startup or heartbeat automation until the workspace baseline and response behavior have been reviewed in the target environment. <br>
Risk: .integrity snapshots can contain sensitive local copies of workspace files. <br>
Mitigation: Treat snapshot files as sensitive local data and restrict access to the workspace and snapshot directory. <br>


## Reference(s): <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenClaw Warden](https://github.com/AtlasPA/openclaw-warden) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local integrity manifests and snapshots, restore files, run git rollback, and rename skill directories when countermeasure commands are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
