## Description: <br>
ZeeLin Deep Research 深度研究是一款 AI 驱动的专业研究辅助平台，支持一句话生成与多步骤生成，提供深度、专家两大研究路径。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and business researchers use this skill to submit research questions to ZeeLin and receive deep or expert-mode research outputs for market, company, policy, product, and investment analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts, generated outputs, and the ZeeLin API key are sent to the ZeeLin service. <br>
Mitigation: Use a dedicated revocable API key and avoid confidential or regulated material unless the deployment has been approved for that data. <br>
Risk: Report delivery workflows may create temporary files or publish generated content into Feishu. <br>
Mitigation: Confirm the intended delivery channel and remove temporary report files after delivery when the runtime does not clean them automatically. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kelcey2023/kelcey-zeelin-deep-research) <br>
- [ZeeLin Deep Research service](https://desearch.zeelin.cn) <br>
- [ZeeLin API key and activity page](https://desearch.zeelin.cn/skill-activity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain-text research answers, with shell commands for setup and execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESEARCH_API_KEY; report delivery may involve generated files or Feishu document links depending on the channel workflow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
