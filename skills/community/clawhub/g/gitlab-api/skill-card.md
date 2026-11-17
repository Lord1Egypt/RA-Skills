## Description:

GitLab API integration for repository operations. Use when working with GitLab repositories for reading, writing, creating, or deleting files, listing projects, managing branches, or any other GitLab repository operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d1gl3](https://clawhub.ai/user/d1gl3)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate GitLab repositories through the REST API, including listing projects, reading files, writing files, deleting files, listing directories, and managing branches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a GitLab token that may have repository write or delete permissions.

Mitigation: Use a least-privilege, revocable token, prefer an environment variable or secure credential store, and keep any file-based token owner-only.

Risk: Helper commands can create, modify, or delete repository files.

Mitigation: Manually approve write and delete operations, especially on protected or default branches, and confirm the target project, path, and branch before execution.

Risk: Credentials could be sent to an unintended GitLab instance if the instance URL is misconfigured.

Mitigation: Require HTTPS for every GitLab URL and verify self-hosted instance configuration before sending authenticated requests.

## Reference(s):

- [GitLab API documentation](https://docs.gitlab.com/ee/api/api_resources.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and helper-script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue authenticated GitLab REST API requests when the helper script is executed by an agent or user.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
