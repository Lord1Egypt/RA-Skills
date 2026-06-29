## Description: <br>
Prepares pull requests by running quality gates, drafting descriptions, and validating tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare pull requests by reviewing workspace state, running quality gates, summarizing changes, documenting tests, and drafting a PR description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad PR or git-related requests and can write or overwrite a PR description at the path provided by the user. <br>
Mitigation: Use it in repositories where PR workflow assistance is intended, choose an explicit output path, and review the generated description before relying on it. <br>
Risk: Quality gate commands may be unavailable or unsuitable for the local project environment. <br>
Mitigation: Run project-specific validation where possible, document any skipped local checks, and record alternative validation in the PR description. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-sanctum-pr-prep) <br>
- [Sanctum Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and checklist items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the PR description to a user-specified path and displays the path and contents for review.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
