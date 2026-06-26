## Description: <br>
Operate outbound voice calls safely with the OpenClaw voice-call plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare clear, task-specific outbound voice-call flows through OpenClaw providers such as Twilio, Telnyx, Plivo, or mock mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live outbound calls can create cost, compliance, or accidental outreach risk if placed without approval or retry limits. <br>
Mitigation: Require explicit approval for live calls when unattended calling is not acceptable, use mock mode first, and set retry or rate limits before production use. <br>
Risk: Voice providers require sensitive credentials for real traffic. <br>
Mitigation: Confirm the voice-call plugin uses scoped provider credentials and keep provider tokens in the plugin configuration rather than in prompts or call scripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/danielsinewe/openclaw-voice-call-playbook) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and configuration keys] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes preflight checks, provider setup notes, call tool actions, troubleshooting guidance, and operational usage boundaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
