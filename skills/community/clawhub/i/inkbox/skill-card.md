## Description: <br>
Send and receive emails and phone calls via Inkbox agent identities. Use when the user wants to check inbox messages, list unread email, view a thread, search mailbox contents, draft/send an email, place an outbound phone call, list call history, retrieve call transcripts, manage vault credentials, or create/set up an Inkbox identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inkbox](https://clawhub.ai/user/inkbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to Inkbox identities for mailbox, phone, call transcript, webhook, and vault credential workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents sensitive authority over Inkbox mailboxes, phone calls, transcripts, identities, and vault secrets. <br>
Mitigation: Confirm every outbound email, phone call, deletion, webhook or WebSocket destination, and credential retrieval before execution. <br>
Risk: Examples and workflows can expose passwords, API keys, private keys, or OTP codes to the agent transcript or terminal output. <br>
Mitigation: Use a minimally scoped Inkbox API key and avoid printing secrets unless the user explicitly needs to inspect them. <br>
Risk: The security scan verdict is suspicious because the integration is powerful and some examples lack clear confirmation guidance. <br>
Mitigation: Install only when the user trusts the skill and the agent with the connected Inkbox account, communications, and vault contents. <br>


## Reference(s): <br>
- [ClawHub Inkbox skill page](https://clawhub.ai/inkbox/inkbox) <br>
- [Inkbox homepage](https://inkbox.ai) <br>
- [Inkbox console](https://console.inkbox.ai) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JavaScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >=18 and INKBOX_API_KEY; agent actions may use Inkbox email, phone, transcript, webhook, WebSocket, identity, and vault APIs.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
