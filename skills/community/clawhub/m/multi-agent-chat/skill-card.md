## Description: <br>
Prevent common failures in multi-agent Discord conversations where multiple AI agents participate in the same channel, including context overflow, token waste, duplicate responses, reaction spam, rate limit collisions, and loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to coordinate multi-bot Discord discussions with stricter turn-taking, short replies, reaction suppression, and human escalation when loops or rate-limit problems appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the skill outside multi-bot Discord discussions can suppress normal conversational behavior through strict turn-taking, terse replies, or NO_REPLY behavior. <br>
Mitigation: Enable it only for agents participating in multi-bot Discord channels where loop prevention and concise responses are desired. <br>
Risk: The skill includes canned reply and silence behavior that may be inappropriate for normal human chats or multilingual channels. <br>
Mitigation: Review channel expectations before deployment and avoid enabling it where those response conventions are unacceptable. <br>
Risk: Misconfigured reaction notifications, shared API keys, or unchecked bot-to-bot loops can increase token usage or cause rate-limit collisions. <br>
Mitigation: Turn off bot reaction notifications, separate API keys per bot where appropriate, and require human input after repeated or prolonged bot-to-bot exchanges. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mupengi-bot/multi-agent-chat) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown with YAML configuration snippet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides behavioral rules, stop conditions, token-budget guidance, and a Discord reaction notification setting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
