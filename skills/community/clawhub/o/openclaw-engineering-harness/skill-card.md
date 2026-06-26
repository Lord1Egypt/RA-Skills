## Description: <br>
Manages an engineering workflow loop for clarifying requests, discovering code, making minimal changes, validating results, and preparing publishable artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4444433333](https://clawhub.ai/user/h4444433333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure coding tasks into clarify, map, implement, verify, and deliver phases. It is intended to keep changes scoped, validated, auditable, and ready for release packaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to read and write local .claude memory files, which may persist project context or user preferences. <br>
Mitigation: Use the skill only in projects where this persistence is acceptable, and review proposed memory updates before they are written. <br>
Risk: The skill includes workflows for repository-changing git commands, including reset, checkout, add, and commit. <br>
Mitigation: Run it in a clean or backed-up working tree and require explicit approval before any repository-changing git action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h4444433333/openclaw-engineering-harness) <br>
- [Publisher profile](https://clawhub.ai/user/h4444433333) <br>
- [Request shape](refs/request-shape.md) <br>
- [Capability model](refs/capability-model.md) <br>
- [Execution loop](refs/execution-loop.md) <br>
- [Memory system](refs/memory-system.md) <br>
- [Export policy](refs/export-policy.md) <br>
- [Release checklist](refs/release-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON configuration and shell command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation plans, change summaries, validation records, distribution summaries, and audit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
