## Description:

Extension for Bitwarden usage: adds an ephemeral HTTPS web unlock helper for rbw (TTL default 10m) so you can unlock remotely without pasting secrets into chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hans00](https://clawhub.ai/user/hans00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to unlock an rbw-backed Bitwarden vault through a short-lived local web helper when direct interactive unlock is unavailable or inconvenient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a vault master password through a public tunnel option and a predictable FIFO/environment handoff.

Mitigation: Use it only on a trusted machine and account, disable the public tunnel unless remote unlock is necessary, and prefer a future version that uses a private per-run FIFO or direct pipe.

Risk: Anyone who obtains the token URL during the TTL window can access the unlock form.

Mitigation: Treat the token URL as secret, share it only with the person unlocking for that one session, keep the default short TTL, and avoid posting it in logs, screenshots, issues, or shared channels.

Risk: Concurrent helper runs or repeated unlock attempts can increase credential-handling exposure.

Mitigation: Avoid concurrent helper runs and wait for an in-progress unlock attempt to complete before retrying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hans00/skills/headless-bitwarden)
- [Cloudflare Tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces short-lived rbw unlock workflow instructions and local helper invocation commands.]

## Skill Version(s):

1.0.2 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
