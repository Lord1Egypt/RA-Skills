## Description: <br>
Git Repo helps agents manage Git repositories, SourceGit integration, ghq cloning, repository migration, bare/worktree recovery, worktree reuse, multi-account SSH setup, and batch repository inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute repository maintenance workflows, including cloning into ghq, registering repositories in SourceGit, converting between regular and bare/worktree layouts, recovering broken worktree metadata, and inspecting multiple repositories for dirty, stashed, or unpushed work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move repositories and edit persistent Git or SourceGit configuration. <br>
Mitigation: Confirm exact source and destination paths, verify repository status, and ensure SourceGit is closed before state-changing filesystem or preference.json edits. <br>
Risk: The skill can remove or delete worktree-related paths during cleanup workflows. <br>
Mitigation: Require explicit user approval before deletion, and inspect branches, stashes, unpushed commits, and path targets before removing worktrees or metadata. <br>
Risk: The skill includes workflows that can place GitHub tokens in command-line clone URLs. <br>
Mitigation: Use credentials only for the immediate clone step, reset remotes to token-free URLs afterward, and prefer credential-helper or SSH-key workflows where practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/git-repo) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [ghq clone workflow](artifact/clone.md) <br>
- [SourceGit integration](artifact/sourcegit.md) <br>
- [Worktree management](artifact/worktree.md) <br>
- [Regular to bare/worktree conversion](artifact/to-bare.md) <br>
- [Bare/worktree to ghq migration](artifact/to-ghq.md) <br>
- [Multi-account SSH mapping](artifact/ssh-key.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run local filesystem and Git state changes when the host agent grants those tools.] <br>

## Skill Version(s): <br>
0.4.1 (source: ClawHub release metadata and CHANGELOG, released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
