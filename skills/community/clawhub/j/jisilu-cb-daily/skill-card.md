## Description: <br>
每日从集思录 webapi 抓取可转债基本数据、强赎倒计时、下修倒计时，支持Cookie管理和本地持久化存储。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cchunter](https://clawhub.ai/user/cchunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual finance-data users can use this skill to collect daily Jisilu convertible bond data, combine basic bond fields with forced-redemption and conversion-price-adjustment countdown data, and save the result as a local CSV file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Jisilu login cookies in a plaintext local file. <br>
Mitigation: Treat references/cookie.json like a password file: restrict local access, keep it out of repositories and backups, monitor cron logs, and delete or rotate the cookies when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cchunter/jisilu-cb-daily) <br>
- [Jisilu website](https://www.jisilu.cn/) <br>
- [Jisilu convertible bond list API](https://www.jisilu.cn/webapi/cb/list/) <br>
- [Jisilu forced-redemption API](https://www.jisilu.cn/webapi/cb/redeem/) <br>
- [Jisilu conversion-price-adjustment API](https://www.jisilu.cn/webapi/cb/adjust/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime output is console text plus a dated CSV file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires requests and pandas, a local Python 3.8+ runtime, and valid Jisilu login cookies stored locally.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
