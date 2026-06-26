## Description: <br>
Gitee operations via OpenAPI and git for repositories, pull requests, issues, comments, and file contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate Gitee repository workflows, including inspecting or creating pull requests and issues, reading repository contents through the API, and working with gitee.com git remotes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated commands can create pull requests, create issues, update files, or push git commits to Gitee repositories. <br>
Mitigation: Use a least-privilege Gitee token scoped to the required repositories and require explicit confirmation before write operations or git push. <br>
Risk: Gitee access tokens may be exposed if printed, pasted into chat, or committed to files. <br>
Mitigation: Keep GITEE_ACCESS_TOKEN in environment or configuration only, and review commands before execution to avoid revealing secrets. <br>


## Reference(s): <br>
- [Gitee OpenAPI documentation](https://gitee.com/api/v5/swagger) <br>
- [ClawHub skill page](https://clawhub.ai/jvy/gitee) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, git, jq, and GITEE_ACCESS_TOKEN for authenticated Gitee operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
