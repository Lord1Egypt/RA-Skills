## Description: <br>
Git Manager helps agents guide advanced Git operations such as bisecting regressions, cleaning up branches, managing stashes, analyzing history, and handling destructive or history-rewriting commands safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository operators use this skill to plan and execute advanced Git diagnostics, branch cleanup, stash recovery, log analysis, and history-rewriting workflows with explicit safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destructive Git commands such as branch deletion, reset --hard, git clean, stash drop/pop, rebase, and forced push can delete work or rewrite history. <br>
Mitigation: Confirm the current branch, HEAD commit, target commit or branch, remote tracking state, and backup plan before approval; require explicit confirmation before execution. <br>
Risk: History-rewriting or forced-push workflows can affect collaborators and remote branches. <br>
Mitigation: Prefer git push --force-with-lease when a forced update is required and verify the remote tracking state before approving the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/openclaw-skill-git-manager) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with Git command blocks and safety checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes explicit confirmations for destructive Git operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
