## Description: <br>
短剧-公众号信息源 helps short drama creators and content operators track trending WeChat official-account articles, cluster them by genre, and generate daily HTML reports with creative trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Short drama scriptwriters, content operators, MCN teams, and official-account owners use this skill to query RedFoxHub data, find popular WeChat short drama articles, review genre trends, and produce local daily reports for content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports may include unescaped external data and are automatically opened locally. <br>
Mitigation: Treat reports as untrusted web content, avoid opening reports from unexpected data sources, and review generated HTML before sharing or using it in sensitive environments. <br>
Risk: The skill requires a RedFoxHub API key and writes report and cache files on the local machine. <br>
Mitigation: Use a scoped, revocable API key, keep it in environment variables, and review local report/cache paths before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/playlet-gzh-feed) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?souce=github) <br>
- [RedFoxHub](https://redfox.hk?souce=github) <br>
- [core_workflow.md](references/core_workflow.md) <br>
- [examples.md](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown summaries and local HTML report files, with Python command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RedFoxHub API key; writes cache data under ~/.workbuddy/cache and reports under ~/Downloads/QoderReports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
