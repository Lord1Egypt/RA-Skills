## Description: <br>
Gitea Workflow defines an issue- and pull-request-centered coordination loop for Implementer and Coordinator agents working across Gitea-based teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project leads, and agent operators use this skill to coordinate multi-agent work through Gitea issues and pull requests while keeping routine status chatter out of group messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because it under-declares credential use while scripts can read a local Gitea token and manage scheduled agent loops. <br>
Mitigation: Review before installing in a real workspace, use a dedicated low-privilege Gitea token per agent, and avoid broad personal access tokens for scheduled agents. <br>
Risk: Cron-based loops can cause agents to act repeatedly on Gitea issues if the cron target, token file, or session target is misconfigured. <br>
Mitigation: Verify the token file path, localhost Gitea endpoint, cron target, and session target before enabling loops. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/gitea-workflow) <br>
- [cron-setup](references/cron-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and cron configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes helper scripts for enabling, disabling, and checking scheduled workflow loops.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, published 2026-06-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
