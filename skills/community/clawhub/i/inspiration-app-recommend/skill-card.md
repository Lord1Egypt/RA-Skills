## Description:

灵感应用推荐助手会从 Product Hunt、GitHub Trending、Hacker News、36Kr、少数派、即刻、V2EX 等平台聚合热门应用、产品和开源项目，分类提炼创意灵感点与商业模式分析，并生成交互式 HTML 可视化推荐报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, product builders, and creators use this skill when they need Chinese-language product inspiration, trend discovery, and actionable app or startup directions from current web sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can render public website content into HTML without clear sanitization.

Mitigation: Review generated HTML before opening or sharing it, and prefer a fixed version that escapes report data before injecting it into the template.

Risk: The generated report loads Chart.js from a CDN in the browser.

Mitigation: Use a bundled or integrity-pinned chart library when handling sensitive reports or running in restricted environments.

Risk: The skill creates a local HTML report file.

Mitigation: Confirm the expected output path and inspect the file before opening it in a browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/inspiration-app-recommend)
- [Report template artifact](artifact/assets/report-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Chinese-language Markdown guidance plus an interactive HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes inspiration-report.html in the working directory and presents it to the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
