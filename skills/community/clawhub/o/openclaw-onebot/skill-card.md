## Description:

OneBot 11 channel plugin for QQ messaging (NapCat/go-cqhttp), with OpenClaw integration for private and group chat, opt-in group reactions, block streaming, voice handling, message batching, allowFrom filtering, shared-directory media staging, and authorized text-command passthrough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xucheng](https://clawhub.ai/user/xucheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw agents to QQ through OneBot 11-compatible frameworks such as NapCat or go-cqhttp. It supports QQ message routing, media handling, voice workflows, reactions, streaming replies, and controlled text-command access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted plugin or QQ bot framework code can affect message handling and media workflows.

Mitigation: Install only from trusted or pinned sources and review the OpenClaw plugin and connected OneBot framework before deployment.

Risk: Exposed OneBot HTTP or WebSocket endpoints can allow unauthorized access to QQ messaging actions.

Mitigation: Use a strong access token and keep OneBot endpoints on localhost or a trusted network.

Risk: Overbroad message-source filters can authorize unintended private users or groups.

Mitigation: Configure allowFrom narrowly for trusted QQ private users or groups instead of using '*'.

Risk: Shared media staging can expose unrelated local files if pointed at broad personal directories.

Mitigation: Set sharedDir to a dedicated media directory rather than desktop, downloads, documents, or other personal folders.

## Reference(s):

- [ClawHub OpenClaw OneBot Skill](https://clawhub.ai/xucheng/skills/openclaw-onebot)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [NapCatQQ](https://github.com/NapNeko/NapCatQQ)
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, configuration, verification, and operational guidance for OpenClaw OneBot channel setup.]

## Skill Version(s):

1.2.15 (source: server release evidence and artifact release.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
