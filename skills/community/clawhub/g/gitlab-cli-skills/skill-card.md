## Description: <br>
Comprehensive GitLab CLI (glab) command reference and workflows for all GitLab operations, including merge requests, CI/CD pipelines, issues, releases, repositories, authentication, variables, labels, milestones, snippets, and other glab commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vince-winkintel](https://clawhub.ai/user/vince-winkintel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide authenticated GitLab CLI work across repository, merge request, issue, CI/CD, release, package, runner, and API workflows. It helps agents choose relevant glab commands, compose shell examples, and apply safety checks before GitLab writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated GitLab commands can act as the wrong visible user or against the wrong host. <br>
Mitigation: Verify the active GitLab account and host before writes, and use separate least-privilege tokens for distinct actors. <br>
Risk: Examples may include state-changing or destructive GitLab operations. <br>
Mitigation: Review the exact target and command before running write, force, delete, yes, or no-verify operations. <br>
Risk: GitLab tokens and environment files can be exposed through logs or shared scripts. <br>
Mitigation: Keep tokens out of logs and version control, restrict local credential files, and avoid embedding secrets in reusable scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vince-winkintel/skills/gitlab-cli-skills) <br>
- [GitLab REST API documentation](https://docs.gitlab.com/api/) <br>
- [GitLab GraphQL documentation](https://docs.gitlab.com/api/graphql/) <br>
- [GitLab Duo CLI documentation](https://docs.gitlab.com/user/gitlab_duo_cli/) <br>
- [NDJSON specification](https://github.com/ndjson/ndjson-spec) <br>
- [JSON Lines](https://jsonlines.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the glab CLI and appropriate GitLab authentication for live operations.] <br>

## Skill Version(s): <br>
1.13.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
