## Description: <br>
Proactive task state management that records task status, background process details, progress, results, and next steps in a local task state file so work can resume after session resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to keep a compact, persistent task snapshot across long-running work, background processes, failures, and session resets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists task and operational context locally, including commands, process identifiers, server names, and progress notes. <br>
Mitigation: Review and prune memory/tasks.md regularly, and do not store secrets, credentials, private customer data, sensitive commands, hostnames, or infrastructure details unless the file is protected by the environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sunshine-del-ux/new-agent-task-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown task-state entries written to memory/tasks.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains a concise state snapshot under 50 lines or 2KB and prunes older completed tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
