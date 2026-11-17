## Description:

Uploads local files or directories to PinMe public IPFS and returns short shareable pinit.eth.limo URLs, with commands for AppKey setup, upload history, unpinning, wallet checks, and logout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to publish local files or static directories to public IPFS through PinMe, receive structured JSON containing a shareable URL, and manage related PinMe account actions such as history, wallet, unpinning, and AppKey configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files uploaded through PinMe are published to public IPFS and may remain accessible even after unpinning.

Mitigation: Use the skill only for files intended to be public; keep upload warnings enabled and require explicit confirmation before upload or unpin operations.

Risk: The skill can automatically install the pinme npm CLI without a pinned package version.

Mitigation: In managed environments, preinstall and audit a known pinme CLI version before enabling the skill.

Risk: A PinMe AppKey may be configured through environment variables or persisted locally for reuse.

Mitigation: Use a limited PinMe account/key, avoid placing the key directly on command lines, store it with restricted permissions, and clear or rotate it when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/pinme-share)
- [PinMe service](https://pinme.eth.limo)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python shell commands and final-line JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, the pinme CLI, and a PinMe AppKey; uploads are limited to 200 MB per file and 1 GB per directory.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
