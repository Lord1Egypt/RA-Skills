## Description:

把 27 份全球医疗器械法规枢纽知识库封装成本地只读 MCP Server，供代理检索法规片段、官方原文链接和待核验标注。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Regulatory engineers, quality teams, and agent developers use this skill to search a bundled medical-device regulatory knowledge base across China, the United States, the European Union, Japan, Latin America, and Southeast Asia. It supports hub listing, keyword search, full hub retrieval, and product classification path lookup for reference workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The regulatory knowledge base may lag current official requirements.

Mitigation: Treat results as reference material and verify final regulatory decisions against the linked official sources.

Risk: The optional REG_HUB_REFS setting can expose a user-selected folder through search and full-document retrieval.

Mitigation: Set REG_HUB_REFS only to a reviewed folder intended for MCP retrieval.

Risk: The skill depends on fastmcp at runtime.

Mitigation: Install in a virtual environment and pin fastmcp to a reviewed version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/global-reg-connector)
- [Reference material index](references/README.md)
- [Lifecycle regulatory hub overview](references/枢纽总览_全生命周期7阶段纲领.md)
- [Registration engineer global materials hub](references/注册工程师资料枢纽.md)
- [Orthopedic surgical instrument global registration path compilation](references/骨科手术器械_全球注册路径汇编.md)
- [Global UDI identification hub](references/UDI全球标识枢纽.md)
- [FDA UDI implementation guide](references/FDA_UDI实施实务.md)
- [EU EUDAMED database guide](references/EU_EUDAMED数据库实务.md)
- [EU MDR post-market surveillance guide](references/EU_MDR上市后监管PMS实务.md)
- [China medical-device MAH outsourced manufacturing guide](references/CN_医疗器械委托生产MAH实务.md)
- [Security results](security_results.json)
- [Security audit report](安全审计报告.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [JSON strings returned by MCP tools, plus human-readable snippets, links, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include regulatory search results, full hub content, classification path hints, official-source links, and explicit verification reminders.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
