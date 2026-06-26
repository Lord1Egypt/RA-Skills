## Description: <br>
Helps users set up a shared Telegram channel so multiple OpenClaw bots can chat with friends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moon-frost](https://clawhub.ai/user/Moon-frost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to configure a shared Telegram channel, add bots as administrators, disable bot privacy where needed, connect OpenClaw to the channel, and save channel rules that keep multi-bot conversations usable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured bots can read and post broadly in the selected Telegram channel. <br>
Mitigation: Use a dedicated private channel, add only trusted people and bots, and avoid sensitive conversations in that channel. <br>
Risk: Saved AGENTS.md channel rules may expose channel details if committed to a public or shared repository. <br>
Mitigation: Keep AGENTS.md private or remove channel identifiers and other sensitive channel details before sharing. <br>
Risk: Multiple bots responding to each other can create message loops or noisy rapid replies. <br>
Mitigation: Use name prefixes, direct-mention response rules, cooldowns, and rate limits before enabling multi-bot conversation. <br>


## Reference(s): <br>
- [OpenClaw Chat With Friends on ClawHub](https://clawhub.ai/Moon-frost/openclaw-chat-with-friends) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown, Text] <br>
**Output Format:** [Markdown guidance with step-by-step setup instructions and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Telegram setup steps, AGENTS.md rule examples, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
