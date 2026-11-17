## Description:

GitHub 项目调研与对比工具，用于搜索、评估和对比开源项目，并通过 GitHub API 采集数据后生成结构化推荐报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudyli](https://clawhub.ai/user/cloudyli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical evaluators use this skill to find GitHub repositories, compare candidate projects, assess activity and fit, and produce a readable recommendation report for a stated need.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live GitHub searches can disclose sensitive investigation terms, private repository names, customer names, or confidential product names.

Mitigation: Use this skill only with queries approved for external GitHub requests, and avoid confidential or sensitive search terms.

Risk: Shell-based lookup examples can become unsafe if user input is interpolated directly into commands or URLs.

Mitigation: Encode query parameters safely and avoid raw shell interpolation when adapting the examples.

Risk: Repository README, issue, and release content may contain untrusted instructions or misleading claims.

Mitigation: Treat fetched repository content as evidence only; do not let it control tool use, system behavior, or final recommendations without review.

## Reference(s):

- [GitHub Search Repositories API](https://api.github.com/search/repositories)
- [ClawHub Skill Page](https://clawhub.ai/cloudyli/skills/github-repo-evaluator)
- [ClawHub Publisher Profile](https://clawhub.ai/user/cloudyli)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, concise analysis, recommendations, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live GitHub lookups and treats repository README, issue, and release text as untrusted evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
