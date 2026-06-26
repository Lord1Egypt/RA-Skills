## Description: <br>
Automates a GitHub Trending to AI summary to knowledge card to WeChat technical blog drafting workflow for technical content production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical bloggers, newsletter authors, and content creators use this skill to discover public GitHub projects, summarize selected repositories, generate developer knowledge cards, and draft long-form technical blog posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on other skills and external tools whose behavior is not fully covered by this artifact. <br>
Mitigation: Review dependent skills separately before deployment and confirm the intended workflow before running broad blog-writing requests. <br>
Risk: GitHub API calls may expose more repository access than needed if run with an over-privileged CLI session. <br>
Mitigation: Use least-privileged GitHub CLI authentication and prefer public-repository access for trend collection. <br>
Risk: Generated blog drafts and images may contain inaccurate, misleading, or unsuitable content for publication. <br>
Mitigation: Manually review generated drafts and images before publishing them to WeChat or other public channels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zlszhonglongshen/github-trending-blog) <br>
- [README](artifact/README.md) <br>
- [Workflow Definition](artifact/workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON-shaped workflow outputs, and generated draft file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates dependent skills for GitHub data collection, summarization, card rendering, and article drafting; generated drafts and images require human review before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
