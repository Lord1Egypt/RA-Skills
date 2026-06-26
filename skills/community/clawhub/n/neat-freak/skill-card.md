## Description: <br>
End-of-session knowledge cleanup that reconciles project documentation and agent memory against the codebase so handoffs stay accurate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkkkhazix](https://clawhub.ai/user/kkkkhazix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill at development milestones or handoff points to audit and update README files, project docs, root agent guidance, and supported agent memory so they match the current code and decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger broadly at handoff or cleanup moments and may modify or delete project documentation and persistent agent memory. <br>
Mitigation: Use it in version-controlled workspaces, request a plan or diff before applying edits, and review proposed documentation and memory changes before accepting them. <br>
Risk: Global configuration edits, memory rewrites, deletions, or changes outside the current project can affect future agent behavior beyond the immediate task. <br>
Mitigation: Require explicit approval before those actions and keep edits scoped to the current project unless broader maintenance is intentionally requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kkkkhazix/neat-freak) <br>
- [Agent memory and configuration paths](artifact/references/agent-paths.md) <br>
- [Documentation synchronization matrix](artifact/references/sync-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation edits, memory or configuration updates, shell command proposals, and concise completion summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose, modify, or delete documentation and memory files when the hosting agent is allowed to edit the workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
