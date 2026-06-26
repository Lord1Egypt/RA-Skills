## Description: <br>
基于波峰波谷分析识别A股股票的压力位和支撑位，生成K线图。使用Baostock获取数据（解决AKShare东财接口限制问题） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wtjjacobj](https://clawhub.ai/user/wtjjacobj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to fetch A-share daily market data, identify support and resistance levels with peak and valley analysis, and generate annotated candlestick charts for stock research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill may send the stock code and date range to public market-data services. <br>
Mitigation: Use only non-sensitive stock symbols and date ranges that you are comfortable sharing with those services. <br>
Risk: The Baostock script may create or overwrite a chart PNG on the user's Desktop. <br>
Mitigation: Review the output path before execution and move or rename any existing chart files that should be preserved. <br>
Risk: Support and resistance levels are technical-analysis outputs and may be incorrect or misleading for investment decisions. <br>
Mitigation: Treat the generated levels and charts as research aids and review them with independent market analysis before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wtjjacobj/pressure-support-candle) <br>
- [压力支撑位识别_设计文档.md](artifact/压力支撑位识别_设计文档.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance, Python execution instructions, printed support/resistance price data, and PNG candlestick chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact public market-data services with the stock code and date range; the Baostock script may create or overwrite a chart PNG on the user's Desktop.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
