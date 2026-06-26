## Description: <br>
公众号搜索爬虫 searches WeChat public-account articles by keyword, shows ranked terminal results, exports CSV files, and can generate an interactive HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, content strategists, and researchers use this skill to search recent WeChat public-account articles for market topics, competitor content, trend tracking, source discovery, and report-ready exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports may expose the user's RedFox API key. <br>
Mitigation: Use a dedicated low-limit key, avoid sharing or syncing generated HTML files, prefer --csv-only when an HTML report is unnecessary, and rotate the key if a report was shared. <br>
Risk: The skill runs a local API proxy while serving the report. <br>
Mitigation: Keep the local server bound to localhost, stop it when finished, and avoid running it on shared or untrusted machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/gzh-search) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox WeChat article search API endpoint](https://redfox.hk/story/api/gzhData/searchArticle) <br>


## Skill Output: <br>
**Output Type(s):** [text, CSV, HTML] <br>
**Output Format:** [Terminal text with CSV files and optional interactive HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RedFox API key; generated HTML reports may embed the API key and use a local API proxy.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
