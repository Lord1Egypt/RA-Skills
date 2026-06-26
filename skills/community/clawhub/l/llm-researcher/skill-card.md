## Description: <br>
LLM paper and project researcher that analyzes LLM-related papers and GitHub projects, then classifies and organizes them by specified categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runshengdu](https://clawhub.ai/user/runshengdu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to track recent LLM papers and GitHub projects from AlphaXiv and GitHub Trending, analyze each item, classify it into a local taxonomy, and produce a traceable research report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runshengdu/llm-researcher) <br>
- [MinerU API documentation](https://mineru.net/apiManage/docs) <br>
- [AlphaXiv hot papers](https://www.alphaxiv.org/?sort=Hot&interval=7+Days) <br>
- [AlphaXiv GitHub-sourced papers](https://www.alphaxiv.org/?source=GitHub&interval=7+Days&sort=Hot) <br>
- [GitHub Trending weekly](https://github.com/trending?since=weekly) <br>
- [Research category taxonomy](references/categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report written to a local output folder, with structured analysis entries and traceable source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, Python, and MINERU_API_KEY for PDF conversion; the report filename uses a YYYYMMDDHHmm timestamp.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
