## Description: <br>
Workspace-level project schedule management for YAML schedules that track modules, milestones, delivery phases, OpenSpec links, and optional Yunxiao sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to review project progress, manage module status transitions, link OpenSpec changes, initialize schedule YAML, and optionally sync schedule modules to Yunxiao. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a local Python environment and install PyYAML from package infrastructure. <br>
Mitigation: Run it in a controlled workspace and review environment changes before using the helper script. <br>
Risk: The skill can edit schedule YAML files in the workspace. <br>
Mitigation: Review diffs before committing or sharing generated schedule changes. <br>
Risk: External Yunxiao sync may send schedule or module information outside the local workspace. <br>
Mitigation: Use sync only after confirming which modules will be sent and after explicit user approval. <br>


## Reference(s): <br>
- [Schedule YAML Schema Reference](references/yaml-schema.md) <br>
- [Workspace Planning on ClawHub](https://clawhub.ai/niracler/nini-workspace-planning) <br>
- [Publisher profile](https://clawhub.ai/user/niracler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON-formatted command results, shell commands, and YAML schedule edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update planning/schedules YAML files and may call a local Python helper for deterministic schedule operations.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
