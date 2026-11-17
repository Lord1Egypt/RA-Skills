## Description:

MediaSync-Claw lets an OpenClaw agent list, link, and stream local MP4 media through a local media server exposed for remote access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yu-libin](https://clawhub.ai/user/yu-libin)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to browse and play MP4 files from a local videos folder through WhatsApp-driven agent requests. It is intended for users who deliberately want remote access to a local media library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make a local media server reachable from the public internet through an unauthenticated tunnel.

Mitigation: Install only when remote media access is intended, run it on an isolated machine or VM, store only non-sensitive media in the videos folder, and add authentication, HTTPS, and rate limits before broader use.

Risk: The skill downloads and runs a native FRP client binary.

Mitigation: Verify frpc manually, avoid broad antivirus exceptions, and keep dependencies and tunnel configuration under review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yu-libin/skills/mediasync-claw)
- [MediaSync-Claw product documentation](https://poly-ai.chat/mediasync-claw)
- [FRP v0.65.0 release used for client download](https://github.com/fatedier/frp/releases/tag/v0.65.0)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [JSON response containing human-facing text and media playback links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local videos folder and a running OpenClaw media server; media files are linked rather than embedded in the agent response.]

## Skill Version(s):

0.1.11 (source: server release metadata; artifact frontmatter says 1.0.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
