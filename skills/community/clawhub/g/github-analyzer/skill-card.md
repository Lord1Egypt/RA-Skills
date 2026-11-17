## Description:

输入项目想法或 GitHub 链接，自动搜索相关开源项目，生成结构化分析报告，并可下载评分最高的前 3 名代码包。

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find, analyze, compare, and optionally download GitHub repositories related to an idea or explicit repository links. It produces structured project reports covering repository activity, language and license metadata, strengths, limitations, fit, and comparative scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, repository names, and any configured GITHUB_TOKEN may be sent to GitHub.

Mitigation: Use the skill only for queries appropriate for GitHub, unset GITHUB_TOKEN when authentication is not needed, or use a minimally scoped token.

Risk: Repository README content is external and may be incomplete, misleading, or untrusted.

Mitigation: Treat generated analysis as a starting point and review repository metadata, source code, and license terms before relying on conclusions.

Risk: Optional downloads can retrieve large or unfamiliar repository ZIP files.

Mitigation: Download only repositories the user has approved and inspect downloaded archives before execution or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/github-analyzer)
- [Publisher profile](https://clawhub.ai/user/antonia-sz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with comparison tables, optional helper-script JSON, and optional downloaded ZIP files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [README excerpts are limited to 3000 characters; GitHub API rate limits depend on whether GITHUB_TOKEN is configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
