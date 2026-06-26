## Description: <br>
Workspace Guardian helps agents keep project workspaces organized by enforcing file placement, naming, memory-tiering, cleanup, and safety-boundary rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golikegod](https://clawhub.ai/user/golikegod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to decide where files belong, validate workspace structure, manage memory files, and run cleanup or validation scripts within a project workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation phrases may cause workspace-management behavior to start during a narrower organization or cleanup request. <br>
Mitigation: Keep actions scoped to the current project and ask the agent to show the exact planned changes before it moves files, runs cleanup scripts, or stops tasks. <br>
Risk: Cleanup behavior can affect files when scripts are run with apply-style execution or when an agent moves scattered workspace items. <br>
Mitigation: Use report-only validation first and require explicit approval before deletion, movement, or broad cleanup. <br>


## Reference(s): <br>
- [Naming Conventions](references/naming-conventions.md) <br>
- [Memory Tiering](references/memory-tiering.md) <br>
- [Safety Boundaries](references/safety-boundaries.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/golikegod/lobster-workspace-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and file-organization recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run workspace validation and cleanup scripts when the user authorizes file-management actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
