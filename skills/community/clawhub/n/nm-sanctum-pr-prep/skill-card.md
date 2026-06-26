## Description: <br>
Prepares pull requests by running quality gates, drafting descriptions, and validating tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare pull requests by reviewing workspace state, running project quality gates, documenting tests, and drafting a concise PR description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate on broad git, PR, or testing requests. <br>
Mitigation: Confirm that the user intends to run a PR-preparation workflow before proceeding. <br>
Risk: The workflow asks the agent to run local formatting, linting, and test commands. <br>
Mitigation: Review commands before execution, resolve failures before continuing, and document any checks that cannot run locally. <br>
Risk: The workflow writes a PR description to a destination path. <br>
Mitigation: Confirm the output path is intentional before allowing the file write. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-pr-prep) <br>
- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown PR description with command summaries, testing notes, and checklist items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the final PR description to a user-specified path and displays it for confirmation.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
