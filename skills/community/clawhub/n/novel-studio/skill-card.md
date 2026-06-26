## Description: <br>
End-to-end Chinese web novel production workflow for turning a novel idea into a structured deliverable project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pallyoung](https://clawhub.ai/user/pallyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors, editors, and agent operators use this skill to run a staged Chinese web-fiction production workflow from concept discovery through planning, drafting, polishing, proofreading, final review, and optional delivery sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Feishu Wiki sync can upload manuscript files to a configured destination space. <br>
Mitigation: Use Feishu sync only after verifying the destination space ID, credentials, and exact files to be uploaded. <br>
Risk: Helper scripts modify the project directory and cleanup flows may delete staging branches. <br>
Mitigation: Keep backups and review branch promotion or cleanup actions before running them on important project data. <br>
Risk: The workflow persists project state and manuscript artifacts on disk. <br>
Mitigation: Install only when a persistent file-backed writing workflow is intended and the project directory is appropriate for generated manuscript content. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [File Structure](references/file-structure.md) <br>
- [State Management](references/state-management.md) <br>
- [Subagent Execution](references/subagent-execution.md) <br>
- [Feishu Sync](references/feishu-sync.md) <br>
- [Narrative Intelligence](references/narrative-intelligence.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON state files, manuscript files, review reports, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file-backed novel project artifacts and may use helper scripts for workflow state, subagent dispatch, validation, revision tracking, and optional Feishu Wiki sync.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
