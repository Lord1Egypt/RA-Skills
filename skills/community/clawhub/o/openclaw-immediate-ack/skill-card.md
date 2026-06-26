## Description: <br>
Use when configuring OpenClaw chat channels to send an immediate acknowledgement before the main reply starts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sallyxie2026](https://clawhub.ai/user/sallyxie2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators configuring OpenClaw chat bots use this skill to add short, language-matched receipt acknowledgements before the full response in Feishu or DingTalk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A visible acknowledgement can imply receipt before the full response has completed. <br>
Mitigation: Keep acknowledgement text limited to receipt and active processing, and preserve normal error handling for the full response path. <br>
Risk: Acknowledgements sent in the wrong language can create a confusing user experience. <br>
Mitigation: Select acknowledgement text from the pool matching the active conversation language or the most recent user message language. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sallyxie2026/openclaw-immediate-ack) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, text] <br>
**Output Format:** [Markdown guidance with bilingual acknowledgement text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, installation steps, or credential handling are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
