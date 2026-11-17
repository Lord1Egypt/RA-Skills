## Description:

GitHub integration for managing repositories, issues, pull requests, and GitHub Actions workflows through a MorphixAI-mediated GitHub API connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to inspect GitHub account and repository state, manage issues and pull requests, and trigger or inspect GitHub Actions workflows from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform repository-changing actions such as creating pull requests, updating issues, and triggering workflows.

Mitigation: Review the target repository, branch, issue or pull request number, workflow file, and environment before executing any mutating action.

Risk: Triggered GitHub Actions workflows may consume CI resources, publish changes, or deploy code depending on repository configuration.

Mitigation: Confirm workflow_dispatch inputs, permissions, and deployment targets before triggering a workflow.

Risk: The integration depends on the MorphixAI plugin and granted GitHub scopes.

Mitigation: Install only if the MorphixAI plugin is trusted and the linked GitHub account scopes are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paul-leo/skills/github-workflow)
- [MorphixAI API keys](https://morphix.app/api-keys)
- [MorphixAI GitHub connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline tool-call examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked GitHub account before GitHub operations can run.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
