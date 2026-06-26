## Description: <br>
Fetches non-military local Chinese government procurement notices from supported platforms, filters them by keyword, enriches details, and generates Excel reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpengle](https://clawhub.ai/user/zhangpengle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and procurement or business-development users use this skill to collect and triage local government bidding opportunities for a selected date, keyword set, and output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live procurement-site bearer tokens and cookies are stored and reused in plaintext .env files. <br>
Mitigation: Use the skill only from a trusted directory, protect generated .env files, avoid pasting real secrets into chat or shell history, and rotate credentials if exposure is possible. <br>
Risk: Proxy settings can route authenticated procurement-site traffic through an untrusted intermediary. <br>
Mitigation: Use proxies only when required and only with trusted proxy endpoints. <br>
Risk: Generated Excel files contain scraped third-party procurement content and may be shared beyond the intended audience. <br>
Mitigation: Review generated workbooks before opening, forwarding, or importing them into other systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpengle/goverment-bidding-fetcher) <br>
- [Beijing Zhongjian Yunzhi government procurement platform](http://zbcg-bjzc.zhongcy.com) <br>
- [Hunan government procurement notice page](http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [CLI text plus Excel workbook (.xlsx)] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Date, keyword filters, detail mode, output path, credentials, and proxy settings affect the generated report.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence; pyproject.toml lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
