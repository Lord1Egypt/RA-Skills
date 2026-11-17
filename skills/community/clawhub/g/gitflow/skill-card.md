## Description:

Automatically push code and monitor CI/CD pipeline status across GitHub and GitLab in one place.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okoddcat](https://clawhub.ai/user/okoddcat)

### License/Terms of Use:


## Use Case:

Developers and engineers use GitFlow to push local commits and monitor GitHub or GitLab CI/CD status, logs, and failures without switching between repository and pipeline dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Push commands can send local commits to a remote GitHub or GitLab repository and trigger CI/CD pipelines.

Mitigation: Review the target remote and branch before using pushflow or any generated push command.

Risk: Pipeline monitoring can consume CI resources and expose build status, URLs, or logs through configured CLI tools.

Mitigation: Confirm CLI authentication, repository permissions, and log sensitivity before streaming or sharing pipeline output.

## Reference(s):

- [ClawHub GitFlow skill page](https://clawhub.ai/okoddcat/skills/gitflow)
- [okoddcat publisher profile](https://clawhub.ai/user/okoddcat)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and gitconfig code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose git push, gh, and glab commands that act on the current repository and remote CI/CD systems.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
