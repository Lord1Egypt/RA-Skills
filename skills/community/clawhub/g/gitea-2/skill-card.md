## Description: <br>
Interact with Gitea using the `tea` CLI. Use `tea issue`, `tea pr`, `tea actions`, and `tea api` for issues, PRs, Actions, and advanced queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[razzeee](https://clawhub.ai/user/razzeee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and repository operators use this skill to ask an agent for Gitea `tea` CLI commands for issues, pull requests, CI/CD Actions data, API queries, and login configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands for listing repository secrets and configuring token-based logins. <br>
Mitigation: Use tokens limited to the needed repositories and scopes, avoid exposing tokens in shared logs or transcripts, and treat repository secret names and login configuration as sensitive. <br>
Risk: Commands may run against the wrong Gitea instance or repository if the login or repository target is incorrect. <br>
Mitigation: Confirm the target Gitea instance, login profile, owner, and repository before running generated commands. <br>


## Reference(s): <br>
- [ClawHub Gitea skill page](https://clawhub.ai/razzeee/gitea-2) <br>
- [Tea CLI Go module](https://code.gitea.io/tea) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Gitea `tea` commands, login setup guidance, and API query examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
