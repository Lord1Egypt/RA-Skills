## Description: <br>
Interact with Kanboard project management via JSON-RPC API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bivex](https://clawhub.ai/user/bivex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Kanboard projects, boards, tasks, comments, subtasks, users, permissions, tags, and related workflow objects through the JSON-RPC API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad write and delete authority over Kanboard data. <br>
Mitigation: Use least-privilege user credentials where possible and require explicit confirmation plus a read-only lookup of affected IDs before remove, disable, permission-change, or bulk operations. <br>
Risk: Kanboard API tokens or passwords could be exposed through logs, transcripts, or insecure transport. <br>
Mitigation: Use HTTPS, keep credentials out of logs and transcripts, and install only when the configured Kanboard server is trusted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Kanboard URL and API credentials, plus curl and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
