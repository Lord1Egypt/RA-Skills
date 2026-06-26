## Description: <br>
Collects pepper oil, Sichuan pepper oil, and related industry-chain data from configured market, pricing, company, government, media, and global report sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MajorLau](https://clawhub.ai/user/MajorLau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to run targeted crawls for pepper oil and Sichuan pepper industry research, including raw material prices, company reports, import/export data, market reports, and competitive landscape information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad multi-site crawling and anti-bot tactics may conflict with site terms, rate limits, robots.txt, login walls, captchas, or Cloudflare blocks. <br>
Mitigation: Run only narrow site or category crawls with permission-aware limits, and do not use proxies, IP switching, or browser automation to bypass access controls or site terms. <br>
Risk: The documented default all-site crawl can create unnecessary traffic and collect data outside the intended research scope. <br>
Mitigation: Prefer category or single-site crawls, use conservative delays, and write outputs to a controlled directory for review. <br>
Risk: Installing dependencies globally with --break-system-packages can alter the host Python environment. <br>
Mitigation: Install dependencies in a virtual environment before running the crawler. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MajorLau/pepper-oil-scraper) <br>
- [Anti-crawl strategy guide](references/anti_crawl_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated data files such as JSON, CSV, and Excel reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Crawler outputs are described as including source_url, crawl_time, and original_text fields with standardized units.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
