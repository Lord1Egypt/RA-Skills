## Description: <br>
Monitors configurable news sources for keyword categories such as geopolitics, oil, and gold, then saves local data and generates summary reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrisingz-crypto](https://clawhub.ai/user/zrisingz-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to configure monitored news sources, classify article titles by keyword categories, and produce local JSON and Markdown summaries for routine market or geopolitical monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured sources may fetch untrusted external news content and save fetched titles, links, timestamps, and keyword tags locally. <br>
Mitigation: Review source URLs and custom headers before enabling them, and treat saved news data and generated reports as untrusted external content. <br>
Risk: The script makes outbound HTTP requests to configured news sites. <br>
Mitigation: Run it only in environments where that network access is expected and permitted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, Python code references, and generated JSON/Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local monitor JSON files and prints a Markdown summary report when executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
