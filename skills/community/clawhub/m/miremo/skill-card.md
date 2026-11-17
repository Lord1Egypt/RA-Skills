## Description:

Access the user's personal Miremo knowledge base and reusable method skills to search notes, browse documents and tags, explore the knowledge graph, save new information, and retrieve method materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansenz42](https://clawhub.ai/user/hansenz42)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect OpenClaw to their own Miremo account, research personal notes and documents, retrieve reusable method skills, and create new memos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected agent can search and read notes, documents, tags, method skills, and knowledge graph data in the authenticated Miremo account.

Mitigation: Install only when the user trusts Miremo and the agent session with that account's content; use a dedicated API key for this integration.

Risk: The skill can create new memos in the connected Miremo workspace.

Mitigation: Confirm user intent before recording information and review created memo IDs or content when write actions matter.

Risk: The Miremo API key grants access through the configured MCP server if exposed.

Mitigation: Keep the API key out of version control, use separate keys for different clients, and revoke unused keys in Miremo settings.

## Reference(s):

- [Miremo homepage](https://www.miremoapp.com)
- [ClawHub skill page](https://clawhub.ai/hansenz42/skills/miremo)
- [ClawHub publisher profile](https://clawhub.ai/user/hansenz42)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown or plain text with retrieved Miremo content, method-skill material, and concise tool-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include memo IDs, workspace context, document section summaries, knowledge graph relationships, and setup configuration snippets.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
