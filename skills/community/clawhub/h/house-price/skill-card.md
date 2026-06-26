## Description: <br>
按城市查二手房与新房参考均价、环比同比及近月走势（可生成列表与 SVG 折线图）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer city-level China house-price questions, including second-hand and new-home reference averages, month-over-month and year-over-year changes, trend lists, and optional chart output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script makes outbound requests to Fangjia pages and trend endpoints. <br>
Mitigation: Use the skill only where public Fangjia lookups are acceptable, keep request volume low, and prefer known city slugs or Fangjia URLs. <br>
Risk: The optional chart mode writes an HTML file to the requested path. <br>
Mitigation: Choose chart output paths deliberately and avoid writing into sensitive or shared locations. <br>
Risk: House-price values are platform reference data rather than official government pricing or investment advice. <br>
Mitigation: Present results with the included reference-only disclaimer and do not use them as the sole basis for purchase or investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/house-price) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jisuapi) <br>
- [查房价 homepage](https://fangjia.fang.com/) <br>
- [City slug reference](city.md) <br>
- [极速数据](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text, with optional SVG or HTML chart output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs house-price summaries in a fixed Chinese template; optional chart mode writes an HTML file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
