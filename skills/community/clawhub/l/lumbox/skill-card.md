## Description: <br>
Lumbox lets agents self-provision email inboxes, send and receive mail, long-poll for OTPs, and use related MCP tooling for browser automation, credential vaulting, and TOTP 2FA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kumard3](https://clawhub.ai/user/kumard3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Lumbox to create agent-owned inboxes, receive verification emails and OTP codes, send or reply to email, and support signup workflows that need email plus credential and 2FA handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad autonomous authority over signup, email, OTP, browser automation, credential vault, and 2FA workflows. <br>
Mitigation: Confirm before allowing account creation, outbound email, browser automation, or credential storage, and prefer scoped inbox keys for subagents. <br>
Risk: The skill handles sensitive credentials and verification artifacts, including LUMBOX_API_KEY, IMAP passwords, OTPs, magic links, and vault contents. <br>
Mitigation: Treat these values as secrets, limit access to agents that need them, store them securely, and rotate or scope keys when delegating work. <br>


## Reference(s): <br>
- [Lumbox REST API Reference](references/API.md) <br>
- [Lumbox Documentation](https://docs.lumbox.co) <br>
- [Agent Signup Guide](https://docs.lumbox.co/docs/agent-signup) <br>
- [ClawHub Skill Page](https://clawhub.ai/kumard3/lumbox) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash commands, REST endpoints, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LUMBOX_API_KEY and may produce JSON containing inbox IDs, email addresses, OTP codes, magic links, API keys, or message metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
