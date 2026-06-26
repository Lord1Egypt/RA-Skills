## Description: <br>
Work with GitLab projects, issues, merge requests, commits, branches, pipelines, and groups via the GitLab API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and manage GitLab projects, issues, merge requests, branches, pipelines, groups, and members through authenticated GitLab API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform state-changing GitLab actions using the connected account, including creating or updating issues, branches, groups, members, and pipelines. <br>
Mitigation: Review the ClawLink preview and approve only actions whose target resource and intended effect match the user's request. <br>
Risk: Project archive/delete, member changes, and pipeline operations can have high operational impact. <br>
Mitigation: Treat these actions as high-impact and require explicit confirmation before execution. <br>


## Reference(s): <br>
- [ClawHub GitLab Skill](https://clawhub.ai/hith3sh/gitlab-repos) <br>
- [Publisher Profile](https://clawhub.ai/user/hith3sh) <br>
- [GitLab API Documentation](https://docs.gitlab.com/api/) <br>
- [GitLab REST API](https://docs.gitlab.com/api/rest.html) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected GitLab account through ClawLink OAuth.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
