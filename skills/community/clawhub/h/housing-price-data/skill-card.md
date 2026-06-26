## Description: <br>
Fetch official Chinese 70-city residential property price index data from the National Bureau of Statistics for housing-price trend questions across supported cities and metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fangtianwd](https://clawhub.ai/user/Fangtianwd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to fetch and summarize official Chinese 70-city residential property price index data for latest-period checks, recent history, and selected city metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public data from stats.gov.cn, so use depends on network access and the availability of that public source. <br>
Mitigation: Install and run it only when external access to stats.gov.cn is acceptable for the workspace. <br>
Risk: Chart or validation report generation can create directories and overwrite files at a chosen output path. <br>
Mitigation: Use a deliberate output path in the workspace and review generated files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fangtianwd/housing-price-data) <br>
- [REFERENCE.md](references/REFERENCE.md) <br>
- [National Bureau of Statistics RSS](https://www.stats.gov.cn/sj/zxfb/rss.xml) <br>
- [Latest validation source sample](https://www.stats.gov.cn/sj/zxfb/202603/t20260316_1962774.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate chart or validation report files when the user requests an output path.] <br>

## Skill Version(s): <br>
2.2.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
