## Description:

Notion Enhanced integrates OpenClaw agents with explicitly shared Notion pages and databases so they can read pages, query databases, create entries, update content, and search workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moikapy](https://clawhub.ai/user/moikapy)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect agents to Notion for knowledge bases, project tracking, content calendars, CRM workflows, and collaborative documentation over pages or databases they explicitly share with the integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has read/write access to Notion pages and databases shared with its integration token.

Mitigation: Use a dedicated Notion integration, share only the minimum required pages or databases, and periodically review or revoke shared access.

Risk: Agent examples and helper scripts include command and credential-handling patterns that require review before installation.

Mitigation: Review setup scripts before use, protect ~/.openclaw/.env with restrictive permissions, and prefer argument-array execution or direct API calls for untrusted titles or JSON values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moikapy/skills/openclaw-notion-skill)
- [Notion API Docs](https://developers.notion.com)
- [Notion Integrations](https://www.notion.so/my-integrations)
- [OpenClaw Docs](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion integration token and access only to Notion pages or databases explicitly shared with that integration.]

## Skill Version(s):

0.1.0 (source: release metadata, SKILL.md frontmatter, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
