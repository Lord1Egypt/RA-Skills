## Description: <br>
短剧-小红书信息源 scans Xiaohongshu short-drama content through RedFoxHub, filters high-engagement posts, clusters genres, and generates Markdown summaries plus HTML daily reports with covers, engagement data, links, and creative insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Short-drama creators, producers, operations teams, MCNs, content strategists, and data analysts use this skill to monitor Xiaohongshu short-drama trends, identify high-performing genres and creators, and produce structured daily reports for content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFoxHub API key and sends authenticated requests to RedFoxHub. <br>
Mitigation: Install only when comfortable granting that access, keep the key in the REDFOX_API_KEY environment variable, and avoid exposing it in code, prompts, logs, or output files. <br>
Risk: The skill writes local reports and cache files and opens generated HTML reports that may load remote images and links. <br>
Mitigation: Run it in an environment where local report and cache creation is acceptable, and treat generated report links and remote media as external content before relying on or sharing them. <br>
Risk: Date-specific requests can fall back to the latest available data when the requested date is not yet updated. <br>
Mitigation: Confirm the exact target date with the user before allowing latest-date fallback behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/playlet-xiaohongshu-feed) <br>
- [RedFoxHub](https://redfox.hk/) <br>
- [RedFoxHub playlet query API](https://redfox.hk/story/api/parseWork/queryPlayletMsgs) <br>
- [Core workflow](references/core_workflow.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response with generated HTML report files and local JSON cache data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; reports and cache files are written locally, and generated HTML reports may load remote images and links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
