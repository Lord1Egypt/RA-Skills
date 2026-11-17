## Description:

Install, enable, verify, pair, and manage PrivateClaw OpenClaw sessions, preferring same-conversation /privateclaw QR replies and falling back to the local CLI when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topcheer](https://clawhub.ai/user/topcheer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and enable the PrivateClaw OpenClaw plugin, configure pairing flows, and troubleshoot encrypted chat sessions across OpenClaw-backed conversations or the local CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a third-party plugin through an unsafe install override using a mutable latest package.

Mitigation: Install only after reviewing the publisher and package source, prefer a pinned and verified package version, and require explicit confirmation before using unsafe install overrides.

Risk: The skill can guide actions that restart OpenClaw, kill sessions, or remove participants.

Mitigation: Confirm the target OpenClaw instance, session, and participant before running restart, killall, or kick commands.

## Reference(s):

- [PrivateClaw provider homepage](https://github.com/topcheer/PrivateClaw/tree/main/packages/privateclaw-provider)
- [PrivateClaw desktop releases](https://github.com/topcheer/PrivateClaw/releases)
- [YourClaw iOS app](https://apps.apple.com/us/app/yourclaw/id6760531637)
- [PrivateClaw Android closed alpha](https://play.google.com/store/apps/details?id=gg.ai.privateclaw)
- [PrivateClaw Android tester group](https://groups.google.com/g/gg-studio-ai-products)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend OpenClaw plugin installation, enablement, restart, verification, pairing, session inspection, and participant removal commands.]

## Skill Version(s):

1.1.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
