## Description: <br>
Cloud-hosted markdown collaboration for agents and humans. One API call to create, one link to share. End-to-end encrypted, no account required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bndkts](https://clawhub.ai/user/bndkts) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and human collaborators use this skill to create, read, update, append, organize, and share cloud-hosted markdown documents and workspaces for notes, task logs, reports, and collaborative documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external cloud markdown service, so sensitive content may leave the user's local environment. <br>
Mitigation: Require explicit approval before uploading sensitive content and confirm the user accepts use of the external service. <br>
Risk: Write and workspace keys can grant broad document or workspace access if stored in ordinary memory, logs, or shared notes. <br>
Mitigation: Prefer read-only keys when possible and keep write and workspace keys in agent-supported config, memory, or secrets storage with restricted exposure. <br>
Risk: Overwrite, append, and delete operations can change or remove shared markdown content. <br>
Mitigation: Use ETags and If-Match for writes, handle conflicts by refetching and merging, and require confirmation before overwrite or delete operations. <br>
Risk: Lost document or workspace keys cannot be recovered and may permanently block access to encrypted content. <br>
Mitigation: Save document and workspace IDs, read keys, and write keys immediately in an approved credential store. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bndkts/molt-md) <br>
- [molt-md website](https://molt-md.com) <br>
- [molt-md skill documentation](https://molt-md.com/skill.md) <br>
- [molt-md API documentation](https://github.com/bndkts/molt-md/blob/main/API.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with REST API examples, JSON responses, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify external cloud-hosted markdown documents and workspaces through the molt-md API.] <br>

## Skill Version(s): <br>
1.1.1 (source: manifest.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
