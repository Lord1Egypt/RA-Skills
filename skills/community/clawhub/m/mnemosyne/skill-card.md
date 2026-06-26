## Description: <br>
Provides an autonomous local memory system that captures, searches, and organizes conversation-derived preferences, decisions, emotions, task context, and conflict updates across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironzheng](https://clawhub.ai/user/ironzheng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent local memory, configurable memory categories, search, and session-level memory analysis to an OpenClaw-style agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous persistent memory can store sensitive details, inferred personal traits, and broad conversation history. <br>
Mitigation: Enable it only intentionally, clear bundled memory files before use, avoid storing secrets or confidential personal and business information, and regularly review saved memory records. <br>
Risk: AGENTS.md or HEARTBEAT automation can persist conversation details without per-entry confirmation. <br>
Mitigation: Do not enable automated session or heartbeat capture by default; prefer manual capture or reviewed analysis until the user has confirmed the memory policy. <br>
Risk: The security guidance flags an inline Python interpolation issue in auto_session. <br>
Mitigation: Avoid auto_session until that issue is fixed; use reviewed auto_analyze output or manual capture instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ironzheng/mnemosyne) <br>
- [User guide](docs/USER_GUIDE.md) <br>
- [Auto Memory protocol](docs/AUTO_MEMORY_PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local Markdown and JSON memory records through bundled CLI scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
