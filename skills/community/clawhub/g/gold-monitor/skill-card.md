## Description: <br>
Queries real-time gold prices, the USD index, WTI crude oil prices, and the gold/oil ratio, then returns market data and investment signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forest-qiao](https://clawhub.ai/user/forest-qiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current precious metals, currency-index, and crude-oil market data and summarize the results. It is also used to compute a gold/oil ratio and present the skill's built-in informational investment signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound read-only requests to market-data services and depends on third-party Python packages. <br>
Mitigation: Install only in environments where outbound market-data requests and the listed Python dependencies are acceptable. <br>
Risk: Market prices and investment signals may be stale, unavailable, or unsuitable for financial decisions. <br>
Mitigation: Treat outputs as informational, surface fetch errors to the user, and verify important financial decisions independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/forest-qiao/gold-monitor) <br>
- [Sina Finance real-time quotes](https://finance.sina.com.cn) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list={code}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary based on JSON returned by the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script returns JSON objects or arrays with prices, changes, units, update times, and error fields when data cannot be fetched.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
