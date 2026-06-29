## Description: <br>
Initializes a stacked branch set from an ordered plan, one branch per slice with parent-child links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn an ordered multi-step implementation plan into a linear stack of Git branches, with each branch based on the previous slice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides creation and checkout of multiple Git branches, which can disrupt local work if used in the wrong repository or with an unclean working tree. <br>
Mitigation: Confirm the target repository, base branch, and clean working tree before running the suggested Git commands. <br>
Risk: The skill includes shell commands that should only be run when they match the user's intended stacked-branch workflow. <br>
Mitigation: Review displayed instructions before execution and only grant tool access for the intended task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-stack-create) <br>
- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides branch naming, prerequisite checks, progress tracking, and stack verification.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
