## Description:

Diagnose failing Proxmint proxy connections. Use when a request through Proxmint returns 407, 403, 500, 502 or 503, a CONNECT tunnel fails, SOCKS5 refuses a connection, the exit IP is in the wrong country, a sticky session changes IP, a browser leaks its real IP through DNS or WebRTC, or a site loads directly but not through the proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prian3003](https://clawhub.ai/user/prian3003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and proxy users use this skill to diagnose Proxmint connection failures, identify likely gateway or client causes, and apply a specific fix with a way to confirm it worked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy credentials could be exposed in chat.

Mitigation: Never request or repeat the password; ask for a username with the real login redacted, and do not echo a password if one is pasted.

Risk: Optional account checks can expose account details, and connection tests consume proxy bandwidth.

Mitigation: Explain these effects before using connected account tools or running a connection test.

## Reference(s):

- [Gateway responses](artifact/references/errors.md)
- [Proxmint documentation](https://proxmint.com/docs)
- [Blocked websites](https://proxmint.com/docs/blocked-websites)
- [Proxmint status](https://proxmint.com/status)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Concise Markdown troubleshooting guidance with concrete fixes and confirmation steps; may include commands or configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
