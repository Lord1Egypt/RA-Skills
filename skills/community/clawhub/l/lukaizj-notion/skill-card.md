## Description:

Notion integration - Manage pages, databases, and content in Notion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukaizj](https://clawhub.ai/user/lukaizj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and productivity users use this skill to let an agent search Notion, query databases, and create pages or database entries in a Notion workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Notion integration token that can access shared workspace content.

Mitigation: Treat NOTION_API_KEY as a secret and share only the Notion pages or databases the agent needs.

Risk: An agent can create pages or database entries in Notion when given valid access.

Mitigation: Confirm page-creation requests before allowing the agent to write content to Notion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukaizj/skills/lukaizj-notion)
- [Publisher profile](https://clawhub.ai/user/lukaizj)
- [Project homepage](https://github.com/lukaizj/notion-integration-skill)
- [Notion integration setup](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [Text, API calls, Configuration, Guidance]

**Output Format:** [JSON-like tool results and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOTION_API_KEY and access only to Notion pages or databases shared with the integration.]

## Skill Version(s):

0.1.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
