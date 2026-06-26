## Description: <br>
Interact with GitLab using the `glab` CLI for merge requests, CI/CD pipelines, issues, releases, and API requests across gitlab.com and self-hosted instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Portavion](https://clawhub.ai/user/Portavion) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent operate GitLab workflows through `glab`, including merge requests, CI/CD pipelines, issues, releases, variables, and API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may use the authenticated GitLab CLI context to perform broad read or write actions. <br>
Mitigation: Use a least-privilege GitLab token and review generated commands before execution. <br>
Risk: Merge approvals, merges, releases, CI retries, variable changes, and non-GET API calls can alter project state or expose private data. <br>
Mitigation: Require explicit approval for those actions and inspect project, repository, and endpoint targets before running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Portavion/glab-cli) <br>
- [Publisher profile](https://clawhub.ai/user/Portavion) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include `glab` commands that read or change GitLab project state, depending on the authenticated CLI context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
