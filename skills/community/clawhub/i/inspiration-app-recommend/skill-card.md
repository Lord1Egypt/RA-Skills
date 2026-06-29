## Description: <br>
灵感应用推荐助手会从 Product Hunt、GitHub Trending、Hacker News、36Kr、少数派、即刻、V2EX 等平台聚合热门应用、产品和开源项目，分类提炼创意灵感、商业模式分析，并生成交互式 HTML 可视化推荐报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product builders, founders, and creators use this skill to research current product trends, find product or application ideas, compare domestic and international sources, and turn the findings into an actionable inspiration report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make several third-party web requests while researching public trend sites. <br>
Mitigation: Use it only for public research topics and avoid including private product plans, credentials, or sensitive customer information in prompts. <br>
Risk: The generated report loads Chart.js from a CDN when opened. <br>
Mitigation: Open the report in an environment where that external dependency is acceptable, or review and adapt the HTML before sharing it in restricted settings. <br>
Risk: The skill writes inspiration-report.html in the working directory. <br>
Mitigation: Check for an existing file with that name before running the skill when preserving prior reports matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/inspiration-app-recommend) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bettermen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Markdown guidance and a generated interactive HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates inspiration-report.html in the working directory and may present the file to the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
