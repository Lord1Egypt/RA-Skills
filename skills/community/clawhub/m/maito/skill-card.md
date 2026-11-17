## Description:

Maito helps agents operate Maito end to end for newsletter publishing, social drafts, subscriber management, attribution review, sponsor workflows, and authenticated Maito MCP tool use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeman14](https://clawhub.ai/user/freeman14)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and publishing operators use this skill to connect an agent to a Maito workspace, prepare newsletter and social content, manage subscribers and attribution, and coordinate sponsor workflows with approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent that reads or updates newsletter, subscriber, analytics, and sponsor information in a Maito workspace.

Mitigation: Review connected Maito permissions before use and limit workspace access to the intended publication and task.

Risk: Publishing, sending, scheduling, subscriber changes, sponsor outreach, or destructive edits could have external or irreversible impact.

Mitigation: Require explicit user approval before those actions and read the current Maito state before making workspace changes.

Risk: Private workspace data, subscriber records, analytics exports, sponsor contracts, credentials, or private URLs could be exposed in public content or committed files.

Mitigation: Keep sensitive Maito data and credentials out of public outputs and committed artifacts.

## Reference(s):

- [Maito MCP Tools Documentation](https://getmaito.com/docs/mcp/tools)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain text workflow guidance, drafts, checklists, status summaries, and Maito-ready handoffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference authenticated Maito tool results when connected; otherwise produces handoff instructions without claiming persistence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
