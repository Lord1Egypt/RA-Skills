## Description:

基于 SearXNG 的多引擎聚合搜索工具，支持分类路由与智能查询，聚合多个搜索引擎结果，适合个人日常信息检索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, students, and researchers use this skill to route search queries across SearXNG-backed general, news, academic, and social search categories and summarize aggregated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill asks for or documents broader local command and file-changing powers than the search purpose explains.

Mitigation: Review before installing, avoid granting write access unless the package is narrowed to search-only behavior, and use the skill only in an environment where local command execution is expected.

Risk: Searches may be sent to a public or configured SearXNG instance.

Mitigation: Use non-sensitive searches or a trusted self-hosted SearXNG instance, especially for private research, business, or user data.

Risk: The artifact describes unsupported export and cache behavior while the security guidance says those features should be clarified.

Mitigation: Treat export, cache, batch query, and custom engine features as unsupported in this release unless a reviewer confirms narrowed behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/internet-search-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Public SearXNG instance referenced by artifact](https://searx.be)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and search query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free edition documents a maximum of 10 results per query and no batch query, export, custom engine configuration, or search cache support.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
