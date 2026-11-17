## Description:

专为调用本地数据接口并生成图表展示定制的 Skill。接收自然语言指令（如“我要最近一年燃油类型为天然气的扭矩占比”），自动提取参数，请求本地接口，生成 HTML 柱状图并返回完整的 HTML 源码。

This skill is ready for commercial/non-commercial use.

## Publisher:

[z904832819](https://clawhub.ai/user/z904832819)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn natural-language chart requests into local API calls and return a complete HTML ECharts bar chart for torque proportion data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact ships an embedded bearer credential for local API requests.

Mitigation: Remove the embedded token before installation and require administrator-provided credentials through a managed secret or environment-specific configuration.

Risk: The script silently falls back to demo data when API requests fail.

Mitigation: Fail clearly on API errors or label fallback data explicitly so users do not mistake sample output for live local API results.

Risk: The skill returns active HTML generated from user-derived parameters and API data.

Mitigation: Validate user-derived parameters and escape values inserted into the HTML title, chart labels, and JavaScript before returning the page.

Risk: The generated HTML loads ECharts from an unpinned CDN URL.

Mitigation: Pin the charting dependency to a reviewed version or bundle the library with the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z904832819/skills/local-api-chart-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/z904832819)
- [ECharts browser library](https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js)

## Skill Output:

**Output Type(s):** [text, code, shell commands]

**Output Format:** [Complete HTML source code returned as plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill extracts required fuel type and time range parameters, accepts optional horsepower, emission, and displacement parameters, and returns HTML between script output markers.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter and meta.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
