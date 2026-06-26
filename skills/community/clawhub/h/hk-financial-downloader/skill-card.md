## Description: <br>
港股公司财报完整下载器。自动从东方财富/同花顺/披露易获取年报、中期报告、季报、招股书，完整报告优先于业绩公告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and financial research agents use this skill to fetch Hong Kong-listed company annual reports, interim reports, quarterly announcements, and prospectuses by stock code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads public financial reports from network sources and stores them locally, which can consume significant disk space during large batch runs. <br>
Mitigation: Review the stock list and year range before execution, monitor local storage, and adjust the script if a configurable output directory or stricter download limits are required. <br>
Risk: Downloaded reports come from external public data sources and may be unavailable, delayed, or incomplete. <br>
Mitigation: Review the generated manifest and source results before relying on the downloaded files for analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/hk-financial-downloader) <br>
- [Eastmoney notices](https://data.eastmoney.com/notices/) <br>
- [10jqka HK stock notices](https://stockpage.10jqka.com.cn/HK{code}/news/) <br>
- [HKEXnews listed company information](https://www1.hkexnews.hk/listedcompany/listedinfo/index_c.htm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance, terminal output, downloaded PDF files, and JSON manifest files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and requests; supports Linux, macOS, and Windows according to release metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
