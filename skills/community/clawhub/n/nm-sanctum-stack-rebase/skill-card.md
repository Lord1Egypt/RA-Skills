## Description: <br>
Cascades a rebase through an entire PR stack after a base PR merges or upstream changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to update stacked pull request branches after a base branch changes, a root PR merges, or a mid-stack branch is revised. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation triggers may surface history-rewrite guidance in unrelated development conversations. <br>
Mitigation: Use the skill only for intentional stacked-PR maintenance and narrow activation language to stacked-PR-specific cases. <br>
Risk: Rebase and force-push workflows can rewrite shared branch history. <br>
Mitigation: Confirm the target stack, start from a clean working tree, fetch remote state first, and review each rebase and force-with-lease push before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-stack-rebase) <br>
- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and checklist-style progress guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Git, GitHub CLI, and optional jj command examples for stacked-branch rebases.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
