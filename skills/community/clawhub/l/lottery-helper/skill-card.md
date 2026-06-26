## Description: <br>
彩票助手查询双色球、大乐透、排列三、排列五、福彩3D、北京快乐8、七乐彩和七星彩的开奖信息，支持按最新期、期数或日期范围查询、导出结果，并生成娱乐用途的推荐号码和计算依据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuce1ge](https://clawhub.ai/user/zhuce1ge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to retrieve recent or historical Chinese lottery draw results, export the data, and request entertainment-only number recommendations with supporting calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact the third-party site 17500.cn to fetch public lottery data. <br>
Mitigation: Run it only in environments where that outbound network access is acceptable and treat the third-party data source as external. <br>
Risk: The skill can write txt, md, xlsx, or sqlite files to user-chosen paths. <br>
Mitigation: Use sensible output paths and review generated files before sharing or importing them elsewhere. <br>
Risk: Lottery recommendations may be mistaken for predictive or financial advice. <br>
Mitigation: Present recommendations as entertainment only and retain the disclaimer that historical results do not affect future random draws. <br>
Risk: Backtesting can take more time and CPU than a normal query. <br>
Mitigation: Ask for user confirmation before running backtests and explain the expected runtime. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zhuce1ge/lottery-helper) <br>
- [Publisher profile](https://clawhub.ai/user/zhuce1ge) <br>
- [彩票数据接口（17500.cn）](references/apis.md) <br>
- [彩票一等奖中奖率](references/odds.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional exported txt, md, xlsx, or sqlite files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can contact 17500.cn for public lottery data and can write user-selected export files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
