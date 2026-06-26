## Description: <br>
Vision-driven iOS device automation using Midscene CLI and WebDriverAgent, operating from screenshots without requiring DOM or accessibility labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanru](https://clawhub.ai/user/quanru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to connect to iPhones or iPads, launch apps or URLs, interact with visible UI, verify screen states, and summarize iOS automation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly control a connected iPhone or iPad. <br>
Mitigation: Use test devices and test accounts, and require explicit confirmation before deleting data, submitting forms, sending messages, making calls, purchasing, changing settings, or logging into sensitive accounts. <br>
Risk: Screen contents may be sent to external model providers during visual automation. <br>
Mitigation: Avoid confidential screens and use limited provider API keys configured only for the intended automation task. <br>
Risk: The workflow depends on the @midscene/ios npm package and sensitive model credentials. <br>
Mitigation: Verify the @midscene/ios package source before use and keep MIDSCENE_MODEL_API_KEY and related provider settings scoped to the least privilege needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/quanru/midscene-ios-automation) <br>
- [Midscene.js documentation](https://midscenejs.com) <br>
- [Midscene model configuration](https://midscenejs.com/model-common-config) <br>
- [Midscene iOS getting started](https://midscenejs.com/ios-getting-started.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference generated screenshots, reports, logs, and converted report files from Midscene runs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
