## Description: <br>
Autonomous Nigerian Airtime distribution agent on Farcaster. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DruxAMB](https://clawhub.ai/user/DruxAMB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External operators and agent users use this skill to manage a Farcaster-based Nigerian airtime giveaway workflow, including public replies, claim-code handling, phone-number submission, and airtime claim commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use preconfigured Farcaster accounts and unreviewed local scripts to post public casts and replies. <br>
Mitigation: Install only when the scripts, account configuration, and reply limits have been audited; keep duplicate-reply checks enabled and require explicit approval for force replies. <br>
Risk: Airtime claims may process phone numbers and claim codes without a clear privacy boundary. <br>
Mitigation: Collect phone numbers through a private or secure path, avoid asking users to post phone numbers publicly, and define retention and deletion rules before operation. <br>
Risk: Airtime distribution can create spending or quota exposure if claim commands run without limits. <br>
Mitigation: Set budgets, rate limits, and approval thresholds for airtime claims, and monitor claim activity before allowing unattended operation. <br>
Risk: Credential handling is implicit because the skill assumes all credentials are already configured. <br>
Mitigation: Use only controlled runtime credentials, restrict their permissions, rotate them when access changes, and do not ask users to provide API keys in chat. <br>


## Reference(s): <br>
- [OpenAirtime ClawHub release](https://clawhub.ai/DruxAMB/open-airtime) <br>
- [OpenAirtime claim site](https://openairtime.fun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus controlled, audited Farcaster and airtime-service credentials before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
