## Description: <br>
妙想提供的股票模拟组合管理系统，支持持仓查询、买卖操作、撤单、委托查询、历史成交查询和资金查询等功能。通过安全认证的API接口实现真实交易体验。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessecq1995](https://clawhub.ai/user/jessecq1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to query and manage a simulated A-share stock portfolio, including holdings, funds, orders, cancellations, and historical trades. It is for simulated trading practice and strategy validation, not real-money trading or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change a simulated financial account through buy, sell, sell-all, cancel, and cancel-all actions. <br>
Mitigation: Require manual confirmation before allowing an agent to execute any order placement or cancellation. <br>
Risk: The MX_APIKEY credential is sent to a configurable API endpoint. <br>
Mitigation: Keep MX_APIKEY secret and leave MX_API_URL on the official provider endpoint unless the replacement endpoint is fully trusted. <br>
Risk: Saved output files may contain account, portfolio, order, or balance details. <br>
Mitigation: Periodically clear saved output files and handle them as sensitive account data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jessecq1995/mx-stock-simulator) <br>
- [Miaoxiang simulated account setup](https://dl.dfcfs.com/m/itc4) <br>
- [Default simulated trading API endpoint](https://mkapi2.dfcfs.com/finskillshub) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text status messages and saved JSON response files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes API responses under /root/.openclaw/workspace/mx_data/output/ with mx_stock_simulator-prefixed filenames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
