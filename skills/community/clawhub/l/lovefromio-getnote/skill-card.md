## Description:

GetNote helps an agent save text, public links, images, tags, and knowledge-base content to a user's Get笔记 account and retrieve notes through list, detail, and semantic search APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to capture personal notes, save links or images, organize tags and knowledge bases, and semantically search previously saved content in a Get笔记 account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private notes and send saved links, images, and note contents to the Get笔记 service.

Mitigation: Use it only for accounts and content approved for Get笔记 processing, and avoid broad auto-save behavior for sensitive links or images.

Risk: OAuth and API key values are long-lived secret material that may be exposed through chat logs, command output, or local configuration.

Mitigation: Treat authorization output as secret, avoid pasting keys into chat, store credentials only in the intended local configuration, and revoke keys from the provider console when no longer needed.

Risk: Shared chats or workspaces may expose private note operations if owner scoping is not configured.

Mitigation: Configure GETNOTE_OWNER_ID before using the skill in any shared chat or workspace so only the intended user can operate the note account.

## Reference(s):

- [Get笔记 API Details](references/api-details.md)
- [Get笔记 Homepage](https://biji.com)
- [Get笔记 Open API Platform](https://www.biji.com/openapi)
- [ClawHub Skill Page](https://clawhub.ai/lovefromio/skills/lovefromio-getnote)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown responses with JSON request bodies, shell commands, API calls, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write OAuth/API credentials to local OpenClaw configuration and may send saved links, images, and note contents to the Get笔记 service.]

## Skill Version(s):

1.7.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
