## Description:

Lobster Distill helps agents package, encrypt, upload, relay, download, decrypt, and install skill packages through human-forwarded text instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaoy01](https://clawhub.ai/user/qiaoy01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to transfer OpenClaw skill packages between agents through a human relay on text-capable messaging channels. It is most relevant when the sender and receiver do not share a direct agent-to-agent integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transferred skills are executable instruction packages that may come from an untrusted sender.

Mitigation: Install only from trusted senders, verify the sender out of band, inspect the package in quarantine first, and scan before deployment.

Risk: The receive workflow downloads, decrypts, extracts, and installs content through shell commands.

Mitigation: Do not run received commands automatically; review commands and destination paths before execution, and do not run them as root or with elevated privileges.

Risk: The relay message includes download credentials and may be forwarded through ordinary messaging channels.

Mitigation: Forward only to intended recipients and use a separate channel for secrets or signed hashes when handling sensitive skills.

Risk: Security evidence notes unsafe shell/name handling that users should review before use.

Mitigation: Use simple expected skill names, avoid sensitive packages unless necessary, and inspect package contents before extraction or installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiaoy01/skills/lobster-distill)
- [Publisher profile](https://clawhub.ai/user/qiaoy01)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a relay message with an admin summary and target-agent instructions; receive workflows may install a downloaded package into a local skills directory.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
