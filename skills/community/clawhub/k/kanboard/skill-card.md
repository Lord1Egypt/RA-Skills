## Description:

This skill lets an agent interact with Kanboard project management through the JSON-RPC API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyang-bsy](https://clawhub.ai/user/liyang-bsy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to let an agent inspect and manage Kanboard projects, tasks, boards, comments, subtasks, users, and permissions through JSON-RPC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on a live Kanboard instance with broad project-management authority, including destructive changes.

Mitigation: Use a dedicated least-privilege automation account where possible and require manual confirmation for delete, user-management, role, membership, and bulk operations.

Risk: Kanboard API tokens are used through HTTP basic auth and can expose project-management access if mishandled.

Mitigation: Use HTTPS with a valid certificate, keep KANBOARD_API_TOKEN out of logs and prompts, and rotate tokens when exposure is suspected.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash code blocks and JSON-RPC payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KANBOARD_URL, KANBOARD_API_TOKEN, curl, and jq.]

## Skill Version(s):

1.0.2 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
