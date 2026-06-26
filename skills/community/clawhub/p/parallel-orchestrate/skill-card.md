## Description: <br>
Parallel Orchestrate turns a gstack implementation plan into wave-based parallel Claude Code subagent work, using isolated git worktrees, wave verification, cherry-pick integration, and handoff to review and ship. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to execute a completed implementation plan through coordinated parallel subagents, isolated worktrees, wave-level verification, and review and shipping handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates substantial repository changes and can create local commits and run records. <br>
Mitigation: Review the generated task plan before approving dispatch and run it from a clean feature branch. <br>
Risk: State files may retain plan names, branch names, result metadata, and analytics records. <br>
Mitigation: Clear local gstack state when plan names, branch names, or result metadata are sensitive. <br>
Risk: The workflow depends on gstack and superpowers sub-skills for review, shipping, worktree isolation, and parallel dispatch. <br>
Mitigation: Verify the referenced gstack and superpowers dependencies before use. <br>


## Reference(s): <br>
- [Parallel Orchestrate repository](https://github.com/kaicianflone/parallel-orchestrate) <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/parallel-orchestrate) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kaicianflone) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command blocks and JSON run records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces orchestration plans, task state, local commits, run records, and handoff guidance for agent execution.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
