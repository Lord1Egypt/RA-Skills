## Description: <br>
Use the openhook CLI to receive real-time webhook events from external platforms and coordinate agent workflows through messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berkantay](https://clawhub.ai/user/berkantay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate the Openhook CLI for receiving webhook events from services such as GitHub, Stripe, Linear, Vercel, and Slack, then route messages among agents through channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and webhook payloads can expose secrets or personal data if logged, shared, or broadcast carelessly. <br>
Mitigation: Use a limited or test Openhook API key where possible, avoid logging or broadcasting secrets and sensitive payload fields, and rotate exposed credentials. <br>
Risk: Webhook subscriptions and agent channels may route events or messages to unintended endpoints or agents. <br>
Mitigation: Subscribe only trusted endpoints and agents, review channel membership before broadcasts, and remove subscriptions that are no longer needed. <br>
Risk: A background daemon can continue listening for real-time events after the intended workflow is complete. <br>
Mitigation: Check daemon status and logs during use, then stop the daemon when real-time listening is no longer needed. <br>


## Reference(s): <br>
- [Openhook website](https://openhook.dev) <br>
- [Openhook dashboard](https://openhook.dev/dashboard) <br>
- [Openhook CLI repository](https://github.com/openhook-dev/openhook-cli) <br>
- [ClawHub release page](https://clawhub.ai/berkantay/openhook-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that can produce streaming text or JSON event output when executed with the Openhook CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
