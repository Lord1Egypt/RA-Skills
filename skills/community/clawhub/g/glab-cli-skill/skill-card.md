## Description: <br>
Guidance for using the GitLab CLI (`glab`) from the terminal for merge requests, issues, CI/CD pipelines and jobs, repository targeting and inspection, clone and fork workflows, self-hosted GitLab instances, and direct GitLab REST or GraphQL API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wufei-png](https://clawhub.ai/user/wufei-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate GitLab projects from the terminal with `glab`, including merge requests, issues, CI/CD pipelines and jobs, repository targeting, authentication, and direct GitLab API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitLab commands can change remote project state, including merges, issue closure, pipeline runs, retries, cancelations, deletes, forks, and raw API actions. <br>
Mitigation: Before executing mutating commands, verify the GitLab host, repository, object ID, branch, and intended effect with the user. <br>
Risk: Authentication tokens used by `glab` may have broad account or project permissions. <br>
Mitigation: Use least-privilege GitLab tokens where practical and stop for re-authentication if `glab auth status` reports missing or invalid credentials. <br>


## Reference(s): <br>
- [glab-cli-skill release page](https://clawhub.ai/wufei-png/glab-cli-skill) <br>
- [Quick Reference](references/quick-reference.md) <br>
- [Authentication and Repository Context](references/auth.md) <br>
- [Merge Requests](references/merge-requests.md) <br>
- [Issues](references/issues.md) <br>
- [CI/CD Pipelines and Jobs](references/ci.md) <br>
- [glab API](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose read-only and mutating GitLab CLI commands; mutating actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
