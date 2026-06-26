## Description: <br>
专为调用本地数据接口并生成图表展示定制的 Skill。接收自然语言指令（如“我要最近一年燃油类型为天然气的扭矩占比”），自动提取参数，请求本地接口，生成 HTML 柱状图并返回完整的 HTML 源码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z904832819](https://clawhub.ai/user/z904832819) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data application builders use this skill to turn natural-language chart requests into parameterized local API calls and return an HTML bar chart for torque proportion data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a bundled API token and security-sensitive local API behavior. <br>
Mitigation: Remove and rotate the embedded token, require a user-provided scoped credential, and review the skill before installation. <br>
Risk: API failures may silently fall back to unlabeled demo data. <br>
Mitigation: Make API failures visible and label or require explicit opt-in for demo data. <br>
Risk: Generated HTML and browser dependencies can expose consumers to unsafe rendering or supply-chain behavior. <br>
Mitigation: Escape user-controlled values before returning HTML and pin or bundle browser dependencies. <br>
Risk: The documented command uses an absolute local path that may not exist for other users. <br>
Mitigation: Use package-relative execution paths when invoking the chart-building script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z904832819/local-api-chart-generator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/z904832819) <br>
- [ECharts browser library](https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, HTML, Code] <br>
**Output Format:** [Complete HTML document containing an ECharts bar chart] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the HTML between explicit start and end markers; chart rendering depends on local APIs and the ECharts CDN.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
