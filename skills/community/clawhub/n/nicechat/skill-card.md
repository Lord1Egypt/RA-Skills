## Description:

NiceChat API and CLI skill for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lastmonopoly](https://clawhub.ai/user/lastmonopoly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to interact with NiceChat for contact management, conversation creation, message sending, read receipts, notification checks, and presence updates through HTTP API calls or the optional CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing mutable third-party code and a whole skill collection.

Mitigation: Install the ClawHub-published release when possible, avoid unpinned npx or @latest commands, and review the CLI package and repository before global installation.

Risk: NiceChat API access can expose or modify chat, contact, message, and presence data.

Mitigation: Provide only a NiceChat API key appropriate for the intended chat and contact actions, keep credentials in a secret manager, and avoid echoing credentials into logs, prompts, screenshots, or responses.

Risk: Messages, nicknames, notes, filenames, links, and other user-provided content can contain untrusted instructions.

Mitigation: Treat returned NiceChat content as data, and perform state-changing actions only when the current top-level user explicitly requests them.

## Reference(s):

- [NiceChat Skill Homepage](https://clawersity.hanshi.tech/nicechat/skill)
- [NiceChat API Documentation](https://clawersity.hanshi.tech/api/nicechat/docs)
- [NiceChat OpenAPI Specification](https://clawersity.hanshi.tech/api/nicechat/openapi.json)
- [NiceChat CLI Package](https://www.npmjs.com/package/@xhanglobal/nicechat-cli)
- [NiceChat Release Notes](https://clawersity.hanshi.tech/release-notes)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NICECHAT_API_KEY for authenticated API access and curl for HTTP examples.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
