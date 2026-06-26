## Description: <br>
Install, configure, inspect, troubleshoot, and operate the terminal-based nchat messenger client for Telegram, WhatsApp, and Signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thisisevgeniy](https://clawhub.ai/user/thisisevgeniy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install, configure, diagnose, and safely operate local nchat profiles for Telegram, WhatsApp, and Signal. It is especially useful for privacy-aware troubleshooting and configuration changes around message cache, account setup, exports, key bindings, themes, proxies, and auto-compose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Account linking, message actions, exports, account removal, and interactive automation can expose private conversations or affect real chat accounts. <br>
Mitigation: Require explicit user approval for the exact account, action, and scope before running those operations. <br>
Risk: Logs, cache files, exports, pairing codes, QR codes, phone numbers, proxy credentials, and local keys may contain sensitive information. <br>
Mitigation: Use the read-only doctor script where possible, avoid broad cache or log inspection, and redact sensitive values before sharing output. <br>
Risk: Auto-compose may send chat history to an external AI service and may incur provider costs. <br>
Mitigation: Keep auto-compose disabled unless the user explicitly asks to enable it and understands the data-sharing and cost implications. <br>


## Reference(s): <br>
- [Nchat Reference](references/nchat-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/thisisevgeniy/nchat) <br>
- [Publisher Profile](https://clawhub.ai/user/thisisevgeniy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and concise diagnostics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Privacy-sensitive actions require explicit user approval; diagnostic output should redact secrets, phone-like values, logs, exports, and message content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
