## Description:

Review GitLab merge requests using a standardized code review template; automatically fetches MR changes, analyzes the diff, and posts a review comment following the template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujinyuan](https://clawhub.ai/user/wujinyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review GitLab merge requests, identify actionable code issues, and prepare a structured review comment. It is intended for MR review workflows where a GitLab CLI session can fetch merge request metadata and changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post generated review comments directly to GitLab merge requests.

Mitigation: Review the generated comment and require explicit approval before posting it to GitLab.

Risk: The workflow can change GitLab CLI host configuration for the current environment.

Mitigation: Limit use to trusted GitLab hosts and prefer per-command host options or temporary configuration over persistent glab config changes.

Risk: Published comments include a fixed OpenClaw attribution that may not match team policy.

Mitigation: Remove or approve the attribution before publishing comments in a team repository.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown review comment with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post the generated review comment to the target GitLab merge request when allowed by the user and GitLab CLI credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
