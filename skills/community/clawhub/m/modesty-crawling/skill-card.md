## Description:

Use for TikTok crawling, content retrieval, and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to generate command-line guidance for collecting TikTok videos and metadata with yt-dlp, exporting datasets, and analyzing engagement patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands may use browser login state or exported cookies to access restricted TikTok content.

Mitigation: Use cookies only for accounts and content you are authorized to access, prefer a dedicated browser profile or tightly permissioned cookie file, and avoid sharing cookie files.

Risk: Scheduled scraping jobs can continue collecting data after the intended task is complete.

Mitigation: Review scheduled jobs before deployment, log activity, and remove any cron entry when it is no longer needed.

Risk: Scraped private or personal data could be uploaded to third-party analysis services.

Mitigation: Analyze data locally when possible and upload exports only when you have permission and trust the provider.

Risk: Unpinned yt-dlp or ffmpeg installations may change behavior over time.

Mitigation: Use a virtual environment or pinned package versions and review updates before recurring scraping runs.

## Reference(s):

- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- [yt-dlp output template reference](https://github.com/yt-dlp/yt-dlp#output-template)
- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-crawling)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and examples for JSON, JSONL, CSV, and downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that download TikTok media or metadata, use browser cookies, write local files, and schedule recurring scraping jobs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
