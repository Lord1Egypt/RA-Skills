## Description: <br>
Generates poster and social image designs by selecting visual-rag templates, filling template slots, and returning rendered PNG images through the disclosed MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zooagentpm](https://clawhub.ai/user/zooagentpm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and agents use this skill to generate promotional posters, event notices, Xiaohongshu covers, and similar campaign images. It guides template search, slot filling, rendering, and quality checks before delivering the final PNG output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Design prompts and any brand, account, date, or campaign details are sent to an external visual-rag MCP service on an ngrok domain. <br>
Mitigation: Avoid confidential, regulated, or unreleased business information unless the service operator and its data handling are trusted. <br>
Risk: Template slot content can be inaccurate or visually flawed if required factual details are missing or text exceeds slot constraints. <br>
Mitigation: Ask for real account, brand, date, or campaign details when required; follow slot limits and inspect the returned quality report and rendered image before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zooagentpm/posterdesign) <br>
- [visual-rag MCP service endpoint](https://syncopated-retractively-anitra.ngrok-free.dev/mcp) <br>
- [v2.5 changelog](artifact/v2.5/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Images, Text, Guidance] <br>
**Output Format:** [PNG images with accompanying text quality report and download links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns render and inspect images; may include slot crop checks and adjustment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
