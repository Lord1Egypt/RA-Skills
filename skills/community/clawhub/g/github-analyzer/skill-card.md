## Description: <br>
输入项目想法或 GitHub 链接，自动搜索或分析相关开源项目，生成结构化项目报告，并可在用户确认后下载评分靠前的代码包。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical evaluators use this skill to find, compare, and analyze GitHub repositories for a project idea or supplied repository links. It produces structured reports covering technology stack, strengths, weaknesses, suitability, and scoring, with optional repository zip downloads after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts GitHub and may use GITHUB_TOKEN from the environment. <br>
Mitigation: Use a minimally scoped read-only GitHub token, unset it when not needed, and run the skill only when GitHub network access is expected. <br>
Risk: Downloaded repository archives may contain untrusted code. <br>
Mitigation: Download only after explicit approval and review or scan downloaded repositories before opening, building, or executing them. <br>
Risk: Repository rankings and reports depend on live GitHub metadata and README content, which can be incomplete or stale. <br>
Mitigation: Validate important findings against the upstream repository before making adoption or procurement decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/github-analyzer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/antonia-sz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown reports, JSON command output, and downloaded zip files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GitHub API data, can use GITHUB_TOKEN when present, and saves approved repository downloads under ~/Downloads/github-analyzer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
