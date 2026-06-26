## Description: <br>
An agent for interacting with GitLab. Supports gitlab.com and self-hosted instances. Requires no GitLab DUO. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrow](https://clawhub.ai/user/xrow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to automate GitLab issue, merge request, repository, and CI/CD workflows through the glab CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act autonomously in GitLab as the token owner and make authenticated repository or account changes without confirmation. <br>
Mitigation: Use a least-privilege GITLAB_TOKEN and restrict installation to test or low-risk projects where possible. <br>
Risk: The skill may push branches, create or modify merge requests and issues, comment, change CI/CD variables, create releases, or merge without asking first. <br>
Mitigation: Review target project permissions before deployment and monitor GitLab activity for changes made by the configured token owner. <br>


## Reference(s): <br>
- [GitLab Agent on ClawHub](https://clawhub.ai/xrow/gitlab-agent) <br>
- [CI Tools Components Catalog for GitLab](https://ci-tools.xrow.de/) <br>
- [xrow Public Skills Project](https://gitlab.com/xrow-public/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and GitLab CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated GitLab actions when used with a configured GITLAB_TOKEN and glab CLI.] <br>

## Skill Version(s): <br>
1.39.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
