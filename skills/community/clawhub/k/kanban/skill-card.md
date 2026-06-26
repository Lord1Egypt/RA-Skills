## Description: <br>
Build multi-project Kanban systems with deterministic board discovery, consistent task processing, and persistent routing memory across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to create and maintain project-specific Kanban boards, route work to the correct board, and preserve task continuity across conversations. It is useful for local task planning workflows that need deterministic card movement, WIP limits, and append-only board logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and maintains local board, registry, memory, and log files. <br>
Mitigation: Choose the intended board location before use and keep writes limited to ~/kanban/ or the selected workspace's .kanban/ directory. <br>
Risk: Kanban cards and memory files can accidentally capture secrets, credentials, private notes, regulated data, or sensitive project details. <br>
Mitigation: Do not store secrets or sensitive data in cards, logs, registry entries, or memory files. <br>
Risk: Automatic activation across projects can update the wrong board when project context is ambiguous. <br>
Mitigation: Use explicit-only or selected-project activation for tighter control, and confirm scope before multi-project updates. <br>


## Reference(s): <br>
- [Kanban skill homepage](https://clawic.com/skills/kanban) <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/kanban) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Board template](artifact/board-template.md) <br>
- [Discovery protocol](artifact/discovery-protocol.md) <br>
- [Processing rules](artifact/processing-rules.md) <br>
- [Memory template](artifact/memory-template.md) <br>
- [Setup guide](artifact/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown board, registry, memory, rules, and log content with concise agent-facing status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes are intended to stay within the selected Kanban scope, either ~/kanban/ or the workspace-local .kanban/ directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
