## Description:

Connects an agent to Notion through Maton to search, read, and query workspace content, with user-approved writes and optional automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Notion users and developers use this skill to search and query their connected workspace. With explicit approval, they can update specific pages, blocks, or databases and set up scoped automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected account can read or change Notion content.

Mitigation: Start with read/list operations and confirm the exact connection and page, database, or block ID before any write.

Risk: Unscoped triggers can monitor more workspace activity than intended.

Mitigation: Scope each trigger to the requested page or database; use workspace-wide monitoring only with explicit consent.

Risk: Hosted functions and destinations can keep running or forwarding events after the initial task.

Mitigation: Create them only on explicit request, disclose their ongoing behavior and destination, and obtain separate approval.

## Reference(s):

- [Notion skill release](https://clawhub.ai/byungkyu/skills/notion-api-skill)
- [Maton](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Notion API introduction](https://developers.notion.com/reference/intro)
- [Notion trigger reference](artifact/references/notion/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with CLI, API, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Maton account; writes and persistent automations require explicit approval.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
