## Description: <br>
GitHub 仓库深度技术解读 — 输入任意开源项目 URL，一键生成架构分析、代码洞察、知识卡片和多平台发布报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leaders, technical researchers, and technical content creators use this skill to evaluate GitHub repositories, understand architecture and dependencies, summarize documentation, gather community feedback, and produce structured reports or shareable knowledge cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository URLs, README content, and derived search queries may be shared with external summarization or community-search tools. <br>
Mitigation: Use the skill primarily for public repositories, and confirm approval before analyzing private, internal, or strategically sensitive projects. <br>
Risk: The workflow depends on separate skills and tools whose implementations are not included in this artifact. <br>
Mitigation: Review and approve the dependent github, summarize, Agent-Reach, and card-renderer skills before relying on the combined workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/github-repo-deep-dive) <br>
- [README.md](README.md) <br>
- [workflow.json](workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Structured Markdown report with summarized analysis, command output, and generated knowledge-card image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository metadata, README summaries, dependency and architecture analysis, community feedback summaries, and batch comparison reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
