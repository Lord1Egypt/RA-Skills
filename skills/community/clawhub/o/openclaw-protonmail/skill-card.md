## Description: <br>
ProtonMail integration via Proton Mail Bridge for reading and sending encrypted emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rvacyber](https://clawhub.ai/user/rvacyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users connect an agent to a local Proton Mail Bridge instance to list, search, read, send, and reply to ProtonMail messages using Bridge-generated IMAP/SMTP credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read mailbox content and send or reply to messages through the configured ProtonMail account. <br>
Mitigation: Install it only for intended mailbox access and review agent actions before outbound email. <br>
Risk: Bridge credentials and OpenClaw session logs may expose sensitive email access or content. <br>
Mitigation: Protect the Bridge password and OpenClaw configuration, and treat workspace or session logs as sensitive. <br>
Risk: The integration depends on Proton Mail Bridge being installed, configured, and running locally. <br>
Mitigation: Verify Bridge is running on localhost and that PROTONMAIL_ACCOUNT and PROTONMAIL_BRIDGE_PASSWORD are configured before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rvacyber/openclaw-protonmail) <br>
- [Proton Mail Bridge](https://proton.me/mail/bridge) <br>
- [Security advisory](docs/SECURITY-ADVISORY-2026-02-26.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Text and JSON-like tool results; setup guidance may include Markdown and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Proton Mail Bridge running locally and PROTONMAIL_ACCOUNT plus PROTONMAIL_BRIDGE_PASSWORD configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
