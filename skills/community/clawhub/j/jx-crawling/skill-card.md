## Description: <br>
Use for TikTok crawling, content retrieval, and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve authorized TikTok videos and metadata with yt-dlp, export JSON or CSV, and analyze engagement or content patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-session cookies may expose account access or private session data. <br>
Mitigation: Use a dedicated low-privilege browser profile or exported cookie file only for authorized scraping, store cookie files privately, and delete them when the task is complete. <br>
Risk: Unattended scheduled scraping may continue after the intended collection window or increase platform rate-limit and policy risk. <br>
Mitigation: Set explicit collection limits, monitor logs, use conservative sleep intervals, and remove any cron job when the scraping task is finished. <br>
Risk: Scraped private, restricted, or sensitive content may be exposed to external APIs during downstream analysis. <br>
Mitigation: Send data to external APIs only after confirming authorization, data sensitivity, and acceptable exposure for the content being analyzed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirkraman/jx-crawling) <br>
- [yt-dlp Supported Sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>
- [yt-dlp Output Template Reference](https://github.com/yt-dlp/yt-dlp#output-template) <br>
- [SkillBoss API Hub Endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with bash, JSON, CSV, and jq examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce yt-dlp commands, cron snippets, jq analysis commands, and data export patterns.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
