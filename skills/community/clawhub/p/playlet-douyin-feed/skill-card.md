## Description: <br>
Short Drama - Douyin Feed tracks Douyin short-drama trends, filters popular works by likes, clusters genres, and generates local HTML reports with engagement data and creative insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, MCN operators, and content analysts use this skill to query Douyin short-drama data, identify trending genres and creators, and generate daily or targeted trend reports for content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a RedFoxHub API key. <br>
Mitigation: Use a revocable API key through REDFOX_API_KEY and avoid passing, printing, logging, or hardcoding the full key. <br>
Risk: The generated HTML report contains externally sourced Douyin content and is opened automatically in the local browser. <br>
Mitigation: Review generated reports before interacting with links or media, and keep browser protections enabled. <br>
Risk: The skill writes local cache and report files. <br>
Mitigation: Inspect and remove files under ~/.workbuddy/cache and ~/Downloads/QoderReports according to local data-retention needs. <br>


## Reference(s): <br>
- [Core workflow](references/core_workflow.md) <br>
- [Usage examples](references/examples.md) <br>
- [RedFoxHub](https://redfox.hk/) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?souce=github) <br>
- [RedFoxHub Douyin short-drama API endpoint](https://redfox.hk/story/api/parseWork/queryPlayletMsgs) <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/playlet-douyin-feed) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML files, Analysis, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summary plus locally generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; writes cache files under ~/.workbuddy/cache and report files under ~/Downloads/QoderReports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
