## Description: <br>
Uses git worktree with coding agents to run multiple development tasks in isolated worktrees in parallel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunwenpinghao](https://clawhub.ai/user/hunwenpinghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to split independent coding tasks across git worktrees, dispatch them to coding agents, and keep merge review under human control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coding agents launched with permission bypass can make broad repository changes. <br>
Mitigation: Prefer normal permission prompts, use isolated feature branches and worktrees, and manually review diffs, tests, pushes, and PRs before merge. <br>
Risk: Loading a full shell profile before agent execution can expose unnecessary environment variables or credentials. <br>
Mitigation: Load only the environment variables required for the task and use least-privilege Git credentials. <br>
Risk: Parallel worktrees can produce conflicting changes when agents modify the same files. <br>
Mitigation: Split task boundaries before dispatch, route changes through PR or MR review, and resolve conflicts before merging. <br>


## Reference(s): <br>
- [Parallel Coding on ClawHub](https://clawhub.ai/hunwenpinghao/parallel-coding) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides workflow guidance and command examples for git worktree-based parallel coding.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
