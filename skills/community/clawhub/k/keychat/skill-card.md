## Description:

Keychat installs sovereign end-to-end encrypted messaging for OpenClaw agents using Signal Protocol over Nostr relays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kcdev001](https://clawhub.ai/user/kcdev001)

### License/Terms of Use:


## Use Case:

External users and developers use Keychat to install, upgrade, and connect encrypted messaging for OpenClaw agents. The skill guides plugin installation, gateway restart, identity retrieval, and contact setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs changing third-party code and runs an auto-downloaded native bridge that is not pinned or verified in the evidence.

Mitigation: Install only if the @keychat-io publisher and binary distribution path are trusted; prefer a pinned reviewed plugin version, documented bridge checksums or signatures, and a clear rollback path.

Risk: Use with sensitive messaging identities or agent accounts could increase impact if the third-party installer or bridge is compromised.

Mitigation: Review the plugin before deployment and avoid sensitive identities until the release, bridge binary, and rollback process are verified.

## Reference(s):

- [Keychat OpenClaw homepage](https://github.com/keychat-io/keychat-openclaw)
- [Keychat app](https://keychat.io)
- [ClawHub skill page](https://clawhub.ai/kcdev001/skills/keychat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks and numbered setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, upgrade, connection, identity, and security warning guidance for OpenClaw Keychat setup.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
