## Description:

Peter Commit Ops automates the handoff from reviewed changes to a commit, branch push, and pull request, connecting review output with CI and PR follow-up workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasilva](https://clawhub.ai/user/chinasilva)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to turn reviewed local changes into a scoped commit, push the working branch, create or report a pull request, and hand off status to CI or PR operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push repository changes or open a pull request, which may expose code or trigger collaborator and CI workflows.

Mitigation: Before execution, verify the reviewed status, branch name, staged file list, commit message, and target remote.

Risk: Automated commit and PR creation can include unrelated local changes if file scope is not checked.

Mitigation: Review the staged file list and prefer task-scoped staging before commit and push.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline shell commands, status fields, links, and blocking reasons when actions cannot complete.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports commit SHA, branch name, PR URL or blocker, and next-step guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
