## Description: <br>
Interact with Gitea using the `tea` CLI. Use `tea issues`, `tea pulls`, `tea releases`, and other commands for issues, PRs, releases, and repository management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericxliu1990](https://clawhub.ai/user/ericxliu1990) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage Gitea repositories, pull requests, issues, releases, actions, webhooks, and related project resources through the `tea` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide repository-changing or destructive Gitea operations, including deleting repositories, publishing releases, creating webhooks, and changing action secrets. <br>
Mitigation: Require explicit user confirmation, verify the target Gitea instance and repository, and preview sensitive commands before execution. <br>
Risk: Commands may rely on Gitea credentials or account privileges that could affect private repositories and organization resources. <br>
Mitigation: Use a least-privileged Gitea token or account and install the `tea` CLI only from a trusted source. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples that require a configured Gitea login and repository context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
