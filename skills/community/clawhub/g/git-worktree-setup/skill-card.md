## Description: <br>
Use when the user explicitly asks to generate or update a git worktree auto-setup script for a repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imsai-sh](https://clawhub.ai/user/imsai-sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent audit a repository, propose a worktree bootstrap plan, and generate a tailored setup script plus hook configuration for fresh git worktrees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated setup scripts and hooks can copy or link local environment files and other sensitive resources. <br>
Mitigation: Review the generated resource declarations, confirm which files contain secrets, and keep copied environment files gitignored before enabling hooks. <br>
Risk: Automatic hook execution may run repository-specific shell setup at agent session or worktree creation time. <br>
Mitigation: Run scripts/setup-worktree.sh manually once, inspect the resulting changes, and enable SessionStart or WorktreeCreate hooks only after the manual run behaves as expected. <br>
Risk: Shared stateful resources can behave incorrectly when multiple worktrees run concurrently. <br>
Mitigation: Choose copy or generated per-worktree state for databases, local service data, and ports when parallel development is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imsai-sh/git-worktree-setup) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [Stack-specific recipes](references/recipes.md) <br>
- [Hook configuration candidates](assets/hook-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash script and JSON configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces repository-specific setup instructions and files; generated scripts should be reviewed and tested before hook automation is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
