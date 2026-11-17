## Description:

ModelScope Api helps agents search, query, and download ModelScope models, datasets, skills, MCP servers, and Studio resources, with account-changing actions requiring explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenghd511](https://clawhub.ai/user/chenghd511)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover ModelScope assets, retrieve MCP server configuration, and produce API, SDK, CLI, and token-setup guidance. It can support downloads and Studio account operations when the user supplies appropriate credentials and explicitly confirms account-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ModelScope install commands may run unreviewed code, including curl-to-bash patterns.

Mitigation: Review install commands and source packages before execution; avoid curl-to-bash installers when a reviewable package-manager or SDK path is available.

Risk: ModelScope tokens can be exposed through shell history, Git URLs, logs, or copied command examples.

Mitigation: Use least-privilege, short-lived tokens through environment variables and avoid embedding real tokens in commands, Git remotes, files, or chat history.

Risk: Studio deploy, delete, secret, and related management operations can change account resources.

Mitigation: Require explicit confirmation for each account-changing operation and verify the target owner, repository, and operation before proposing or running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenghd511/skills/modelscope-api)
- [Publisher profile](https://clawhub.ai/user/chenghd511)
- [Project homepage from release metadata](https://github.com/Chenghd511/modelscope-api-skill)
- [Project support from release metadata](https://github.com/Chenghd511/modelscope-api-skill/issues)
- [ModelScope OpenAPI document](https://modelscope.cn/.well-known/openapi.json)
- [ModelScope access token page](https://www.modelscope.cn/my/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON snippets, Python examples, shell commands, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ModelScope API responses or proposed commands; account-changing actions require explicit user confirmation.]

## Skill Version(s):

1.0.4 (source: server release metadata, SKILL.md frontmatter, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
