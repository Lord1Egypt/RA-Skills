## Description: <br>
自动监控多个交易所的IPO动态，对比新增或更新记录，并将报告推送到飞书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qishenfeng-sys](https://clawhub.ai/user/qishenfeng-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial professionals, investment teams, and individual investors use this skill to monitor IPO status changes across configured Chinese, Hong Kong, and U.S. exchanges and receive concise Feishu alerts or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IPO reports and operational alerts may be sent to a configured Feishu workspace. <br>
Mitigation: Confirm the workspace is approved for this content and verify webhook destinations before enabling scheduled runs. <br>
Risk: Webhook URLs are secrets that could allow unwanted message posting if exposed. <br>
Mitigation: Store webhook values outside shared source files and rotate them if they are accidentally disclosed. <br>
Risk: Scheduled scraping can repeatedly query external exchange sites and may send repeated alerts during failures. <br>
Mitigation: Run in test mode first, review scheduler frequency, and keep alert cooldown settings enabled. <br>
Risk: Dependency versions may change over time when installed from broad requirement ranges. <br>
Mitigation: Pin reviewed, patched dependency versions for long-running deployments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qishenfeng-sys/ipo-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/qishenfeng-sys) <br>
- [SSE IPO Listings](https://www.sse.com.cn/listing/renewal/ipo/) <br>
- [SZSE IPO Project Dynamics](https://www.szse.cn/listing/projectdynamic/ipo/) <br>
- [BSE Project News](https://www.bse.cn/audit/project_news.html) <br>
- [HKEX Newly Listed Securities](https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities) <br>
- [HKEX Listing Applications](https://www.hkexnews.hk/app/appindex.html) <br>
- [NASDAQ IPO Calendar](https://www.nasdaq.com/market-activity/ipos) <br>
- [NYSE IPO Center](https://www.nyse.com/ipo-center/ipo-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown-style IPO change reports, with configuration values and shell commands for setup or scheduling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print test-mode previews locally, write logs and SQLite cache files, and send Feishu webhook messages when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
