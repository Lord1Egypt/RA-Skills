## Description: <br>
Use for TikTok crawling, content retrieval, and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content researchers use this skill to build TikTok collection workflows with yt-dlp, including downloads, metadata export, filtering, incremental archiving, and scheduled scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide users to use browser cookies or exported cookie files for restricted TikTok content. <br>
Mitigation: Use cookies only from accounts you control, treat cookie files as secrets, and avoid committing, sharing, or pasting them into logs or prompts. <br>
Risk: The skill may produce or process scraped TikTok data that can include user-generated content and engagement metadata. <br>
Mitigation: Store exports in controlled locations, review downstream sharing, and avoid sending scraped data to optional external APIs unless the transmitted data is understood and approved. <br>
Risk: The skill includes scheduled scraping examples that can run repeatedly without close supervision. <br>
Mitigation: Review cron jobs and scripts before enabling them, confirm target handles and storage paths, and monitor logs and rate-limit behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-crawling) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/modestyrichards) <br>
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>
- [yt-dlp output template reference](https://github.com/yt-dlp/yt-dlp#output-template) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, bash scripts, JSON/CSV export patterns, jq snippets, and cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent in producing local download commands, metadata extraction commands, analysis snippets, and scheduled scraping configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
