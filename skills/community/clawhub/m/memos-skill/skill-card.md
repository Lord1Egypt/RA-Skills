## Description:

Memos Skill helps agents configure and operate a Memos note system, including creating, listing, searching, updating, deleting, commenting on, reacting to, and attaching files to memos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomait](https://clawhub.ai/user/xiaomait)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal-knowledge-management users use this skill to let an agent manage notes in a configured Memos instance through authenticated API calls. It supports routine memo capture, search, organization, attachments, comments, reactions, and selected administrative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses a Memos bearer token for API access.

Mitigation: Use an environment variable or secret manager when possible; if config.json is used, restrict it to owner-only permissions, keep it out of version control, and prefer limited-scope tokens.

Risk: The skill can modify private notes through delete, bulk edit, upload, and token-creation workflows.

Mitigation: Require explicit user confirmation before destructive or broad mutation actions, and verify the target Memos instance before executing authenticated requests.

Risk: The agent can read and search private note contents once configured.

Mitigation: Install only for trusted Memos instances and only when the user accepts agent access to private note content.

## Reference(s):

- [Memos project website](https://usememos.com)
- [ClawHub skill page](https://clawhub.ai/xiaomait/skills/memos-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON, JavaScript, HTTP, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute authenticated Memos API calls when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
