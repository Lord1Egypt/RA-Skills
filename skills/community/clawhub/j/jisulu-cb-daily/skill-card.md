## Description: <br>
每日从集思录抓取可转债基本数据、强赎倒计时、下修倒计时，支持 Cookie 管理和本地持久化存储。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cchunter](https://clawhub.ai/user/cchunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and investors use this skill to automate daily collection of Jisilu convertible-bond data, including base bond fields, forced-redemption countdowns, downward-revision countdowns, and local CSV reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide and persist a live Jisilu browser session cookie, which can grant access equivalent to the active web session. <br>
Mitigation: Use a dedicated or low-privilege Jisilu session where possible, restrict filesystem access to references/cookie.json, delete the file after collection, and rotate or log out of the session if exposure is suspected. <br>
Risk: Authenticated requests may fail if the cookie expires, is revoked, or no longer has access to member-only data. <br>
Mitigation: Check failures before relying on generated CSV output and refresh the cookie only through the documented Jisilu login flow. <br>
Risk: Financial market data collected from remote endpoints may be incomplete, delayed, or affected by interface changes. <br>
Mitigation: Review generated CSV summaries and source endpoint behavior before using the output for decisions or downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cchunter/jisulu-cb-daily) <br>
- [Jisilu](https://www.jisilu.cn/) <br>
- [Jisilu convertible bond list endpoint](https://www.jisilu.cn/web/data/cb/list) <br>
- [Jisilu forced redemption endpoint](https://www.jisilu.cn/web/data/cb/redeem) <br>
- [Jisilu downward revision endpoint](https://www.jisilu.cn/web/data/cb/adjust) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CSV files, JSON cookie configuration, and Markdown/plain-text status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated CSV files under output/ and may create references/cookie.json for the Jisilu login cookie.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
