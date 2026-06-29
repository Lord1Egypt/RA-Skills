## Description: <br>
Tracks viral Bilibili short-drama content through RedFox API queries, clusters themes, and produces local HTML daily reports with structured trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Short-drama creators, MCN operators, production teams, and content strategists use this skill to monitor Bilibili short-drama trends, compare themes, identify high-engagement works, and generate daily trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and calls redfox.hk to fetch Bilibili short-drama data. <br>
Mitigation: Use a revocable API key stored in REDFOX_API_KEY, review the key scope before use, and avoid exposing credentials in prompts, logs, code, or generated files. <br>
Risk: The skill creates local report and cache files and may open generated HTML in the browser. <br>
Mitigation: Review generated HTML reports before sharing them and run the skill in an environment where local report and cache output paths are acceptable. <br>
Risk: The security guidance notes that the subscription feature and some command examples are unreliable in this version. <br>
Mitigation: Prefer one-off report generation for important workflows and verify the installed script path and output directory before relying on scheduled or subscription behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/playlet-bili-feed) <br>
- [Publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [RedFox API key setup](https://redfox.hk/settings/api-keys?souce=github) <br>
- [Core workflow](references/core_workflow.md) <br>
- [Usage examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown trend summary, shell command examples, and locally generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; creates local cache/report files and may open generated HTML reports in the browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
