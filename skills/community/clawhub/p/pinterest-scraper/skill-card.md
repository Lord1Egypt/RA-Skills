## Description: <br>
Full-featured Pinterest image scraper with infinite scroll, quality options, Telegram integration, duplicate detection, resume support, and verbose logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KeXu9](https://clawhub.ai/user/KeXu9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to run a Pinterest scraping workflow for boards, profiles, or search results, with configurable image quality, deduplication, resume support, local file output, and optional Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scraper weakens HTTPS certificate verification for image downloads. <br>
Mitigation: Review the code before use and consider restoring certificate verification before running it on trusted systems. <br>
Risk: Telegram delivery can upload locally downloaded JPG files using a bot token and chat ID. <br>
Mitigation: Keep Telegram credentials out of shell history and logs, use only the intended chat, and verify the files before enabling Telegram delivery. <br>
Risk: Scraped images may be subject to third-party rights or platform restrictions. <br>
Mitigation: Confirm that you have permission to download, store, and redistribute the selected images before running or sharing outputs. <br>
Risk: The skill writes images, logs, and resume state to a local output directory. <br>
Mitigation: Use a fresh, dedicated output directory and review generated files before reuse or sharing. <br>


## Reference(s): <br>
- [ClawHub Pinterest Scraper release page](https://clawhub.ai/KeXu9/pinterest-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/KeXu9) <br>
- [Pinterest Scraper homepage](https://github.com/KeXu9/pinterest-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with command examples and CLI option guidance; runtime output includes downloaded JPG files, logs, and optional Telegram media batches.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create a local output directory, scrape.log, and .scrape_state.json for resume and deduplication.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
