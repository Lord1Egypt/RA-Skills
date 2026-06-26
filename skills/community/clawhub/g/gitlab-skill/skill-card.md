## Description: <br>
GitLab operations including creating and cloning repositories, listing projects, managing issues, merge requests, branches, commits, and pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pickbert](https://clawhub.ai/user/pickbert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work with GitLab projects through API and git operations, including repository creation, project browsing, issue and merge request workflows, branch and commit inspection, and pipeline status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitLab access tokens may be exposed during normal use, especially when credentials are stored in files or embedded in HTTPS clone URLs. <br>
Mitigation: Use a dedicated least-privilege token, prefer environment variables or a chmod 600 user config file, avoid storing real credentials in scripts/config.json, and avoid the private HTTPS clone helper until token-in-URL handling is fixed. <br>
Risk: TLS verification can be bypassed for internal GitLab instances, which can expose authenticated traffic on untrusted networks. <br>
Mitigation: Do not use the insecure mode on untrusted networks; fix certificate trust and keep TLS verification enabled for normal use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pickbert/gitlab-skill) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, links, confirmations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute authenticated GitLab API calls and git commands when invoked by an agent with configured credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
