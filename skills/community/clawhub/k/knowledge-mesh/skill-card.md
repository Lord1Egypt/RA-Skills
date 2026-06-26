## Description: <br>
知识网格 / Knowledge Mesh is a cross-platform knowledge search aggregator for unified search across GitHub, Stack Overflow, Discord, Confluence, Notion, Slack, Baidu, and Obsidian with self-learning result ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering teams, and knowledge workers use this skill to search, rank, deduplicate, monitor, and export knowledge from external services and local notes. It is especially suited for technical Q&A, open-source issue research, internal documentation lookup, Obsidian vault search, and recurring topic monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search private services and local notes, and it may persist local files, notes, and query history. <br>
Mitigation: Install only when the publisher is trusted, scope tokens to the smallest necessary repositories, workspaces, channels, pages, or vaults, avoid indexing secret-bearing or confidential locations, and periodically review or delete the local data directory. <br>
Risk: Search terms may be sent directly to configured external services. <br>
Mitigation: Avoid submitting sensitive queries unless the destination service is approved for that data, and configure only the knowledge sources required for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanjing5024064/knowledge-mesh) <br>
- [API endpoints reference](references/api-endpoints.md) <br>
- [Search syntax guide](references/search-syntax.md) <br>
- [GitHub REST search documentation](https://docs.github.com/en/rest/search) <br>
- [Stack Exchange API documentation](https://api.stackexchange.com/docs) <br>
- [Discord developer documentation](https://discord.com/developers/docs) <br>
- [Confluence Cloud REST API documentation](https://developer.atlassian.com/cloud/confluence/rest/) <br>
- [Notion API reference](https://developers.notion.com/reference) <br>
- [Slack search.messages API documentation](https://api.slack.com/methods/search.messages) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured search, monitoring, ranking, and export results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Markdown reports, CSV exports, JSON command responses, ranked result lists, topic digests, search suggestions, and Mermaid trend charts depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
