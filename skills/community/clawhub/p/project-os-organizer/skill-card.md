## Description: <br>
Privacy-first, chat-first project manager for vibe coders. Track projects, capture updates, and resume work across local folders, Claude/Codex, and GitHub with explicit opt-in controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LDodee](https://clawhub.ai/user/LDodee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-assisted builders use this skill to inventory active projects, capture progress and next steps, inspect activity, and resume work from local folders, Claude/Codex sessions, and opt-in GitHub context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local scanning and optional chat/session indexing can expose more project and conversation context than expected. <br>
Mitigation: Keep chat indexing and home-directory discovery disabled unless the user explicitly opts in and understands the folders being scanned. <br>
Risk: Direct shell environment loading can change trusted repository, sync, dashboard, and storage behavior. <br>
Mitigation: Review `.project_os_env` before use and avoid changing trusted repository variables unless the source is intentionally approved. <br>
Risk: Natural-language commands can mutate project state, including status changes, item updates, and project merges. <br>
Mitigation: Use extra care with mutating requests and ask for clarification when a project name or destructive action is ambiguous. <br>
Risk: Remote install and background dashboard execution increase local execution authority when explicitly enabled. <br>
Mitigation: Leave remote install disabled by default and start background services only after confirming the user requested the dashboard. <br>


## Reference(s): <br>
- [Project OS Organizer on ClawHub](https://clawhub.ai/LDodee/project-os-organizer) <br>
- [Project definition](references/project-definition.md) <br>
- [Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown responses with optional shell command snippets and configuration values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local memory snapshot and start a local dashboard when explicitly requested.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
