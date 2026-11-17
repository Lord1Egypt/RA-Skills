## Description:

One-shot Notion workspace scaffolder that creates or adopts a Second Brain page and its Reading List and Inbox databases using Notion MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prakhar728](https://clawhub.ai/user/prakhar728)

### License/Terms of Use:

MIT-0

## Use Case:

Notion users and agent operators use this skill to set up a minimal Second Brain workspace structure. It creates or adopts the parent page and two child databases without adding methodology content or unrelated pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or move Notion workspace objects without asking the user to confirm the exact target location or existing databases first.

Mitigation: Before installation or execution, share the Notion integration only with the page where the Second Brain setup should live.

Risk: Visible databases named Reading List or Inbox may be adopted or moved automatically.

Mitigation: Avoid running the skill in a workspace where unrelated Reading List or Inbox databases are visible to the integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prakhar728/skills/notion-second-brain-setup)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Text]

**Output Format:** [Notion MCP tool calls followed by a plain-text setup report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or adopts one Notion page and two child databases; may move existing Reading List or Inbox databases under the Second Brain page.]

## Skill Version(s):

0.4.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
