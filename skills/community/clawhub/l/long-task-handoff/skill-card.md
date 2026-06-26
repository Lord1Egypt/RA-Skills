## Description: <br>
Long Task Handoff helps agents create, update, recover, and validate concise Markdown handoff packets for long-running work when context compaction or session transfer occurs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollis9087](https://clawhub.ai/user/hollis9087) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve restart-critical task state during long coding or analysis sessions. It creates or refreshes handoff files with current goals, changed state, test status, next actions, risks, and recovery instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated handoff files persist local task context, file paths, branch state, and summaries of user instructions. <br>
Mitigation: Review generated handoffs before committing or sharing a repository, and remove sensitive or unnecessary context. <br>
Risk: The skill writes handoff artifacts into the workspace or a temporary location during long tasks. <br>
Mitigation: Install it only where persistent handoff files are desired, and keep the generated files within the intended workspace boundary. <br>


## Reference(s): <br>
- [Long Task Handoff Protocol Reference](artifact/references/protocol.md) <br>
- [Secret Pattern Validation Rules](artifact/references/secret-patterns.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/hollis9087/long-task-handoff) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown handoff files with JSON command responses and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped handoff files and an ACTIVE.md pointer in the workspace or temporary location when invoked.] <br>

## Skill Version(s): <br>
0.3.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
