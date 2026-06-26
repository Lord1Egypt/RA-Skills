## Description: <br>
Intelligent workplace inspection system with guided setup, configurable inspection tasks, AI-powered image analysis, and Feishu alerting. Use when you need to monitor employee presence, conduct security patrols, or perform automated visual inspections of workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsygcn](https://clawhub.ai/user/wsygcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and workplace administrators use this skill to configure camera-based inspections, analyze images against user-defined criteria, and send alerts for employee presence, security patrol, or facility inspection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workplace camera monitoring can involve employee privacy, notice, consent, retention, and local legal requirements. <br>
Mitigation: Deploy only in authorized environments with documented employee notice and consent, approved retention practices, and local legal review. <br>
Risk: Camera access tokens and Feishu recipients can expose sensitive images or alerts if stored or shared carelessly. <br>
Mitigation: Use least-privilege camera tokens, restrict alert recipients, confirm config-file storage, and rotate any token that may have been saved in plaintext. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wsygcn/intelligent-inspection) <br>
- [EZVIZ Cloud capture API endpoint](https://open.ys7.com/api/open/cloud/v1/capture/save) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, JSON, Text] <br>
**Output Format:** [Text guidance with JSON configuration and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local camera configuration, inspection prompts, AI analysis status, and alerting instructions for Feishu or configured channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
