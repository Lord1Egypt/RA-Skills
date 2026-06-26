## Description: <br>
Renders Chinese market charts from standardized bars data with moving averages, MACD indicators, ECharts templates, and HTML, PNG, or JSON export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forevershu](https://clawhub.ai/user/forevershu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to generate Chinese futures market chart artifacts from standardized bar data for review, reporting, or downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated market chart files are written under output/generated/images. <br>
Mitigation: Run the skill in a workspace where that output path is expected and review generated HTML, PNG, and JSON files before sharing them. <br>
Risk: PNG export launches a local Chrome or Chromium binary for headless screenshots. <br>
Mitigation: Use a trusted browser installation and use the no-PNG mode when browser-based rendering is not acceptable. <br>
Risk: Generated HTML loads ECharts from a CDN. <br>
Mitigation: Open generated HTML only in environments where CDN loading is permitted, or adapt deployment to use a reviewed local ECharts asset. <br>
Risk: Market data comes from a separate AkShare-based dependency. <br>
Mitigation: Review the AkShare data dependency and source suitability before relying on the rendered market data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/forevershu/market-chart-renderer) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/forevershu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML, PNG, and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated chart artifacts under output/generated/images and can skip PNG export when Chrome or Chromium is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
