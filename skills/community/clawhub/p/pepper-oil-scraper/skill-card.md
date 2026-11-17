## Description:

Collects pepper oil and Sichuan pepper industry-chain data across prices, reports, company filings, trade data, standards, media, and global market sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majorlau](https://clawhub.ai/user/majorlau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect and standardize pepper oil and Sichuan pepper market, pricing, company, government, media, and global market data. It can help produce datasets and Excel reports for industry research and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawling protected or restricted sites may violate site terms or access controls.

Mitigation: Review target-site terms, robots.txt, and permissions before crawling; do not use proxy rotation, IP switching, browser automation, or similar guidance to bypass CAPTCHA, Cloudflare, signatures, or access controls.

Risk: The documented dependency command can affect the user's system Python environment.

Mitigation: Install dependencies only inside an isolated virtual environment and avoid the documented --break-system-packages option.

Risk: Collected data can include insecure HTTP sources or untrusted page content.

Mitigation: Prefer HTTPS-only sources and preserve source_url, crawl_time, and original_text fields so outputs remain auditable.

Risk: Generated Excel workbooks can carry spreadsheet-specific risks when opened or shared.

Mitigation: Sanitize Excel exports before opening or distributing generated workbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/majorlau/skills/pepper-oil-scraper)
- [Anti-crawl guide](references/anti_crawl_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and shell commands; generated datasets may be JSON, CSV, or XLSX.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collected records include source_url, crawl_time, and original_text fields when the scraper produces standardized data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
