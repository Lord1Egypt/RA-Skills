## Description: <br>
Complete Notion API for databases, pages, blocks, users, search, comments, and property types with pagination and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide Notion API operations for databases, pages, blocks, users, search, comments, properties, pagination, and error handling through their own Notion integration token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion integration token can expose or modify workspace data if it is shared too broadly or leaked. <br>
Mitigation: Use a least-privilege Notion integration, share only the pages and databases needed, and keep NOTION_API_KEY out of chats, logs, screenshots, and repositories. <br>
Risk: Create, update, archive, delete, or comment operations can change real Notion workspace content. <br>
Mitigation: Review any command that writes to Notion before running it against production workspace content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/notion-api-integration) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill Homepage](https://clawic.com/skills/notion-api-integration) <br>
- [Setup - Notion API Integration](artifact/setup.md) <br>
- [Databases - Notion API](artifact/databases.md) <br>
- [Pages - Notion API](artifact/pages.md) <br>
- [Blocks - Notion API](artifact/blocks.md) <br>
- [Pagination - Notion API](artifact/pagination.md) <br>
- [Error Handling - Notion API](artifact/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is intended to be adapted to the user's Notion workspace and integration permissions.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
