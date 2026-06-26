## Description: <br>
Monitor NDRC website news releases for oil price adjustment announcements on 10-working-day windows and emit Feishu-ready notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manucode2000-max](https://clawhub.ai/user/manucode2000-max) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Operators and developers use this skill to monitor China NDRC oil price announcements, skip non-window days, and generate concise notification output when potential price adjustments are detected. <br>

### Deployment Geography for Use: <br>
Global, with China-specific source data and scheduling assumptions. <br>

## Known Risks and Mitigations: <br>
Risk: Notification and scheduling behavior is under-documented, including how Feishu delivery is triggered. <br>
Mitigation: Review SKILL.md and oil_price_monitor.py before installation, then document the actual scheduler, stdout capture behavior, credentials, and Feishu delivery path used in the target environment. <br>
Risk: The skill runs web scraping, local cache writes, and a subprocess path that should be understood before deployment. <br>
Mitigation: Confirm the exact commands, cache location, subprocess behavior, and network destinations before enabling scheduled execution. <br>
Risk: Dependencies are version-ranged rather than pinned to reviewed builds. <br>
Mitigation: Pin and audit requests, beautifulsoup4, lxml, and the required chinese-workdays skill before installing in a production environment. <br>
Risk: Extracted price adjustment details may be incomplete or incorrect if the NDRC page layout changes or scraper matching is too broad. <br>
Mitigation: Treat generated alerts as advisory and verify material price-change information against the official NDRC announcement before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manucode2000-max/ndrc-oil-price-monitor) <br>
- [NDRC news releases](https://www.ndrc.gov.cn/xwdt/xwfb/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notification text and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes a local adjustment-window cache, fetches NDRC web pages, and normally skips execution on non-window days.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
