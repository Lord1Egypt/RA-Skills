## Description:

Clips web pages to Notion by fetching a URL with Chrome CDP, converting rendered HTML to Markdown and Notion blocks, and saving the result to a selected Notion database or page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ewingyangs](https://clawhub.ai/user/ewingyangs)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to save rendered web pages into a Notion database or page. It supports public pages and user-assisted capture for pages that require login, lazy loading, or manual preparation before capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Notion integration token and can write captured content into selected Notion pages or databases.

Mitigation: Use a least-privileged Notion integration and grant it access only to the pages or databases needed for clipping.

Risk: The skill can open arbitrary pages, including logged-in or private pages, and copy their rendered content into Notion.

Mitigation: Avoid clipping localhost, intranet, cloud metadata, admin, regulated, or sensitive logged-in pages.

Risk: The documented command path can auto-install and run Node dependencies on first use.

Mitigation: Review or preinstall dependencies deterministically before first use instead of relying on automatic install or npx execution.

Risk: The skill uses a persistent Chrome profile for capture sessions.

Mitigation: Use a sandboxed browser profile and avoid sharing cookies or sessions that expose sensitive accounts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ewingyangs/skills/notion-clipper-skill)
- [Notion integration setup](https://notion.so/my-integrations)
- [Notion API base URL](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [Markdown, API calls, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown converted to Notion API block objects, with terminal status messages and Notion page creation or append operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Chrome or Chromium browser, Node.js with tsx, a Notion integration token, and access to the selected Notion database or page.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
