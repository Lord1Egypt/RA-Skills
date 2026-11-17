## Description:

Notion API助手 - 创建和管理Notion页面、数据库，支持笔记和知识管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-management users can use this skill to set up a Notion API helper for creating pages, querying databases, updating page properties, retrieving pages, and searching workspace content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can read or modify selected Notion pages and databases when a user supplies a Notion integration token.

Mitigation: Grant the integration access only to the required pages or databases and confirm before running create_page or update_page examples.

Risk: Embedding a Notion token in source code or examples can expose workspace access.

Mitigation: Store the Notion token outside source code, such as in a local secret store or environment variable.

Risk: Installing an unreviewed dependency version can introduce supply-chain risk.

Mitigation: Use a virtual environment and pin a reviewed notion-client version before deployment.

## Reference(s):

- [Notion integrations setup](https://www.notion.so/my-integrations)
- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-notion)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied Notion integration token and the notion-client Python package.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
