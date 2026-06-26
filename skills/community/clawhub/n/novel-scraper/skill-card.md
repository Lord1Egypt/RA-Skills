## Description: <br>
Novel Scraper helps agents fetch online novel chapters with curl and BeautifulSoup, handle pagination and chapter ranges, skip non-novel content, and save formatted TXT files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to direct an agent through batch downloading public web-novel chapters, filling paginated chapters, checking chapter continuity, and storing merged TXT outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound web requests to novel websites and downloads page content. <br>
Mitigation: Use it only for public pages you intentionally want to download, and review target URLs before running scraper commands. <br>
Risk: Downloaded chapters, cache, logs, and progress files may remain on disk. <br>
Mitigation: Clear ~/.openclaw/workspace/novels, the skill state and log folders, and /tmp/novel_scraper_cache when retained content is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuzhihui886/novel-scraper) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Release Notes](artifact/RELEASE_NOTES.md) <br>
- [Supported Site Configuration](artifact/configs/sites.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, Text] <br>
**Output Format:** [Markdown guidance with inline bash commands; scraper scripts produce formatted TXT novel files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloaded chapters are saved locally and may be merged into multi-chapter TXT files.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata and changelog, released 2026-04-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
