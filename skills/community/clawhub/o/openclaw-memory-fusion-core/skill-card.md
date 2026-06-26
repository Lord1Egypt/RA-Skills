## Description: <br>
Build and operate a unified OpenClaw memory system that combines native Markdown memory, project memory, structured event memory, migration from older PROJECTS.md/improvements.md layouts, memorySearch configuration, and upgrade-safe maintenance workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhongtw1979](https://clawhub.ai/user/zhongtw1979) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, migrate, audit, and maintain a unified memory layout with dry-run previews, manifests, rollback data, and semantic retrieval support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rollback and credential or configuration handling are broader than some users may expect. <br>
Mitigation: Run dry-run previews first, inspect generated manifests before rollback, avoid rollback with untrusted or edited manifests, and pass API keys only when accepting that they may be written into config. <br>
Risk: Auto-capture, semantic sync, and session-memory options may process sensitive memory content. <br>
Mitigation: Review memory files for sensitive information before enabling those options and install the skill only when persistent OpenClaw memory reorganization is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhongtw1979/openclaw-memory-fusion-core) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write OpenClaw memory files, manifests, checkpoints, semantic digests, and configuration when apply flags are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
