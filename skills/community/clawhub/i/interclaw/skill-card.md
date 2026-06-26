## Description: <br>
Secure, sequenced, PGP-signed email mesh for agent-to-agent coordination via plain email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachlagden](https://clawhub.ai/user/zachlagden) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use InterClaw to coordinate OpenClaw instances over email with PGP signing, optional encryption, sequencing, acknowledgements, and gap detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to trust helper scripts with mailbox credentials, PGP signing authority, archives, and optional background mail handling, but the ClawHub artifact does not include those executable scripts. <br>
Mitigation: Install only from a complete source package where the referenced scripts are present, pinned, and reviewed before use. <br>
Risk: SMTP, IMAP, and PGP secrets are required for normal operation. <br>
Mitigation: Use a dedicated email account, app-specific SMTP/IMAP passwords, and a dedicated PGP key; avoid passing passwords directly on the command line. <br>
Risk: Polling and auto-ACK behavior can create ongoing background mail processing. <br>
Mitigation: Enable cron, systemd polling, or auto-ACK only when continuous processing is intended and monitored. <br>
Risk: Gmail may rewrite MIME content in ways that corrupt PGP signatures. <br>
Mitigation: Use a PGP-safe provider or self-hosted mail pipeline documented for preserving signed message content. <br>


## Reference(s): <br>
- [InterClaw ClawHub listing](https://clawhub.ai/zachlagden/interclaw) <br>
- [InterClaw Protocol v3](artifact/docs/protocol-v3.md) <br>
- [Example configuration](artifact/config/example.env) <br>
- [Himalaya v1.1.0 download](https://github.com/pimalaya/himalaya/releases/tag/v1.1.0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GnuPG, email account credentials, a PGP key, and an IMAP/SMTP-capable mail pipeline for the described workflows.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
