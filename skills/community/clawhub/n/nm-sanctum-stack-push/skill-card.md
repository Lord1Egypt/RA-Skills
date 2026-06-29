## Description: <br>
Pushes all branches in a stack and opens or updates one dependent PR per slice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to publish stacked Git branches and create or update a dependent GitHub pull request for each slice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to push branches, create draft pull requests, and post GitHub comments using the user's authenticated GitHub permissions. <br>
Mitigation: Use it only when those repository changes are intended, keep pull requests as drafts until reviewed, and inspect generated commands before execution. <br>
Risk: Stack publication can affect public review state if the wrong branches, bases, titles, or summaries are used. <br>
Mitigation: Confirm the stack prefix, base branch, branch order, and pull request body content before publishing or updating the stack. <br>


## Reference(s): <br>
- [Nm Sanctum Stack Push on ClawHub](https://clawhub.ai/athola/skills/nm-sanctum-stack-push) <br>
- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides branch pushes, draft pull request creation, and stack summary comments for GitHub workflows.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
