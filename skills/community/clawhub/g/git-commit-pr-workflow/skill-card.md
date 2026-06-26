## Description: <br>
Guides an agent through safe branch checks, commits, pushes, and pull request creation or updates with a concise summary and test plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to turn an existing working tree into a pushed branch and a ready pull request while preserving safe git practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent could commit unrelated or sensitive changes while preparing the pull request. <br>
Mitigation: Inspect branch state and staged diffs before committing, stage only relevant files, and avoid committing secrets. <br>
Risk: Git operations could overwrite shared history or affect a default branch. <br>
Mitigation: Create a feature branch when needed, avoid destructive git commands unless explicitly requested, and do not force push to default branches. <br>
Risk: A pull request body could misstate the actual diff or test coverage. <br>
Mitigation: Base the title, summary, and test plan on the inspected diff and clearly report any tests that were not run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wimi321/git-commit-pr-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with shell commands and pull request body text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces git workflow steps, commit and push actions, and a concise pull request summary and test plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
