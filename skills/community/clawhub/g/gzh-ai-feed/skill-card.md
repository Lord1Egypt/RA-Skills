## Description: <br>
AI公众号信息源 scans AI WeChat public-account articles, identifies popular items by read count, clusters them into topics, and generates a styled HTML daily report with metrics, cover images, search, and subscription support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content-curation teams use this skill to generate daily AI WeChat article reports, inspect high-read articles by topic, and search the collected article set through the generated local report experience. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and can store or embed sensitive credential material in local configuration or generated report behavior. <br>
Mitigation: Prefer REDFOX_API_KEY over a plaintext config file, avoid sharing generated reports without review, and rotate the API key if local files may have been exposed. <br>
Risk: The generated report can run a localhost search proxy while the process remains open. <br>
Mitigation: Use --no-open when interactive search is not needed, and close the report process when finished. <br>
Risk: --subscribe installs an OS-level scheduled task for recurring report generation. <br>
Mitigation: Use --subscribe only when scheduled execution is intended, review the created LaunchAgent or crontab entry, and remove it with --unsubscribe when no longer needed. <br>
Risk: Reports are written to the local filesystem and may contain article metadata, links, and usage context. <br>
Mitigation: Choose an appropriate output directory and review generated HTML before sharing it outside the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/gzh-ai-feed) <br>
- [RedFox API key setup](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, HTML, Files, Shell commands, Configuration] <br>
**Output Format:** [Terminal text plus a generated HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RedFox API key; writes reports under the configured output directory, defaulting to ~/Downloads/QoderReports; optional search uses a localhost proxy while the report process stays open.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
