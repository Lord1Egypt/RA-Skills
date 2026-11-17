## Description:

Intelligent workplace inspection system with guided setup, configurable inspection tasks, AI-powered image analysis, and Feishu alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsygcn](https://clawhub.ai/user/wsygcn)

### License/Terms of Use:

MIT-0

## Use Case:

Facilities, security, and operations teams use this skill to configure camera-based workplace inspections, request AI analysis of captured images, and send Feishu alerts for employee presence, patrol, or facility-check scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workplace camera monitoring may create privacy, consent, or compliance obligations.

Mitigation: Use only after confirming that monitoring is approved for the environment and aligned with applicable workplace policies and regulations.

Risk: Camera access tokens or credentials may be stored in local JSON configuration.

Mitigation: Treat camera tokens as sensitive secrets, restrict host and directory permissions, and avoid storing real tokens on shared or unmanaged systems.

Risk: Captured images or analysis results may be sent to AI providers or Feishu.

Mitigation: Review configured providers and alert channels before use and limit captured data to the minimum necessary inspection scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsygcn/skills/intelligent-inspection)
- [EZVIZ Cloud capture API endpoint](https://open.ys7.com/api/open/cloud/v1/capture/save)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include camera configuration prompts, inspection task guidance, AI analysis text, and alerting instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
