## Description: <br>
Handle advanced git workflows and recovery tasks. Use when the user needs help with interactive rebase, commit cleanup, conflict resolution, reflog recovery, cherry-pick, stash, worktree, bisect, submodule vs subtree decisions, sparse checkout, branch archaeology, or undoing dangerous history mistakes in real repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarinRowe](https://clawhub.ai/user/DarinRowe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute advanced Git workflows, including history cleanup, conflict resolution, recovery from repository mistakes, and repository-structure decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested Git commands can alter repository history or working-tree state, especially reset, rebase, and force-push operations. <br>
Mitigation: Review commands before running them, inspect repository state first, and create a backup branch before risky history edits. <br>
Risk: Rewriting shared history can disrupt collaborators or overwrite remote work. <br>
Mitigation: Avoid rewriting shared branches unless the tradeoff is explicit, and prefer force-with-lease over force-push when a rewritten remote update is intended. <br>


## Reference(s): <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>
- [History Surgery](references/history-surgery.md) <br>
- [Recovery](references/recovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety checks, recommended command sequences, rollback paths, and shared-history warnings when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
