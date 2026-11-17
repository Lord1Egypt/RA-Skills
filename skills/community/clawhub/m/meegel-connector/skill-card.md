## Description:

Connect to Meegle via MCP service, support OAuth authentication, and enable querying and managing work items, views, etc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wadxm](https://clawhub.ai/user/wadxm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Meegle through an OAuth-authenticated MCP service so it can query views, to-dos, and work items and perform work-item operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector handles Meegle OAuth credentials, including a remote flow where credential material may be synchronized with agent assistance.

Mitigation: Prefer browser OAuth where the agent does not inspect credential contents; require explicit user confirmation for credential operations, avoid sending authorized credentials through chat or attachments, store credentials only in ~/.mcporter/credentials.json, and clean temporary files promptly.

Risk: The skill runs @lark-project/meego-mcporter through npx without a pinned version, so the tool or its dependencies could change after review.

Mitigation: Verify the npm package version before use and consider pinning @lark-project/meego-mcporter to a reviewed version with locked dependencies and restrictive permissions on ~/.mcporter/credentials.json.

Risk: Authorized use can read Meegle data and create, modify, or transfer work items.

Mitigation: Install only for workspaces where this level of Meegle access is acceptable, and review agent actions before executing work-item mutations.

## Reference(s):

- [@lark-project/meego-mcporter npm package](https://www.npmjs.com/package/@lark-project/meego-mcporter)
- [Meegle OAuth authorization help](https://meegle.com/b/helpcenter/product/5rifl7a7)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, Meegle OAuth, and ~/.mcporter/credentials.json for authorized use.]

## Skill Version(s):

1.0.9 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
