## Description:

Set up and troubleshoot a secure hybrid OpenClaw Gateway on a VPS with a paired local node for GPU, browser, macOS, local-file, and model workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkfaris94](https://clawhub.ai/user/jkfaris94)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to connect a local machine to a remote OpenClaw Gateway, approve node pairing and capabilities, route remote execution through least-privilege allowlists, troubleshoot connectivity, and plan upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Join links, Gateway tokens, setup codes, or keys could be exposed through chat, logs, or shell history.

Mitigation: Treat these values as secrets, store a single-use join URL privately with restrictive file permissions, and avoid copying credentials into transcripts or logs.

Risk: A Gateway exposed beyond the private tailnet can expand the attack surface for node pairing and remote access.

Mitigation: Keep the Gateway bound to loopback, publish through a tailnet-only Tailscale Serve route, avoid Funnel or public port 18789 exposure, and keep trusted proxy settings narrow.

Risk: Approving the wrong request or widening remote exec allowlists can grant agents unintended node capabilities.

Mitigation: Inspect each pending or reapproval request before approving its exact request id, approve only needed capabilities, and restrict exec allowlists to named absolute-path binaries with approval on miss.

## Reference(s):

- [Upgrade Notes](references/upgrade-notes.md)
- [remote-node-ssh companion skill](https://github.com/jkfaris94/remote-node-ssh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes security checks, approval criteria, and upgrade verification steps.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
