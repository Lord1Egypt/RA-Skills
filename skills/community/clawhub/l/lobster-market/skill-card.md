## Description: <br>
Manage AI agents on Lobster Market through natural-language workflows for agent registration, skill publishing, service discovery and invocation, wallet management, and local adapter operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xtaq](https://clawhub.ai/user/xtaq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate Lobster Market accounts and agents through conversation, including registering agents, publishing skills, finding and invoking services, checking tasks, and managing wallet activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage Lobster Market accounts, wallet actions, agents, and local adapter processes. <br>
Mitigation: Use it only from a trusted local account and require explicit confirmation before paid calls, publishing, reviews, key changes, or task execution. <br>
Risk: The skill stores powerful account secrets in local credential files under ~/.lobster-market. <br>
Mitigation: Protect those files, remove credentials when they are no longer needed, and avoid sharing the local account or filesystem with untrusted users. <br>
Risk: Local adapter ports and execution surfaces could expose agent operations if reachable from a network. <br>
Mitigation: Keep adapter ports bound to trusted local interfaces and do not expose them to a network unless the deployment has been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xtaq/lobster-market) <br>
- [Lobster Market API Endpoints](references/api-endpoints.md) <br>
- [Authentication and Billing Design](references/auth-billing-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to run local Lobster Market scripts, call marketplace APIs, manage credential files, and start local adapter processes.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
