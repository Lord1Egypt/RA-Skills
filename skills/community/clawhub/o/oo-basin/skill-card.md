## Description:

Basin (usebasin.com). Use this skill for ANY Basin request — reading, creating, updating, and deleting data. Whenever a task involves Basin, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to manage Basin projects, forms, webhooks, and submissions through their connected OOMOL account. It provides action-specific command examples and approval guidance for changes and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation uses downloaded code whose behavior is not established by this release.

Mitigation: Review and verify the CLI installation separately before allowing automatic setup.

Risk: Startup skill synchronization may change skills used by other agents.

Mitigation: Consider disabling cross-agent startup skill synchronization with the documented OO_SKILLS_SYNC_DISABLED control.

Risk: Basin write and deletion actions can change or remove account data.

Mitigation: Keep the skill's approval requirements for every write and deletion.

## Reference(s):

- [Basin](https://usebasin.com)
- [Basin API access documentation](https://docs.usebasin.com/account-management/api-access/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas and example payloads vary by the requested Basin operation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
