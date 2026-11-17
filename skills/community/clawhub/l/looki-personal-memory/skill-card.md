## Description:

Retrieve the user's personal memories saved by Looki, including moments of daily activities, daily and weekly life summaries, chat history and summaries, health reports, AI-generated journals such as illustrated diaries, comics, and vlogs, and a memory overview, through MCP (if available) or the Looki CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[looki](https://clawhub.ai/user/looki)

### License/Terms of Use:

MIT-0

## Use Case:

People using an authorized Looki account can retrieve saved personal context to recall activities, review summaries and health observations, continue past chats, or find saved journals. The agent should retrieve only the records needed for the request and respect authorization in shared conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal, health, location, and chat records may expose sensitive information, especially in shared conversations.

Mitigation: Use an authorized Looki account, retrieve only records and fields needed for the request, and confirm authorization before sharing records in a shared conversation.

Risk: External Looki CLI and MCP behavior was not audited.

Mitigation: Use only capabilities exposed by the authorized connection, discover current MCP schemas, and check the installed CLI version and command help before querying.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/looki/skills/looki-personal-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Retrieved Looki records and summaries as text or Markdown, with requested media or saved files where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Record and file availability depends on the connected Looki MCP server or installed, authenticated Looki CLI.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
