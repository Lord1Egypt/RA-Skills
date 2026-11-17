## Description:

Local Auto Emoji detects conversation emotion, generates personalized emoji images from a user avatar, and sends matching emoji media in OpenClaw chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdkmail](https://clawhub.ai/user/wdkmail)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw operators use this skill to add automatic emotion-based emoji responses to chat workflows, including avatar-based emoji generation and marker-triggered media insertion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Avatar images, generated emoji assets, and emotion logs may reveal personal or behavioral information.

Mitigation: Require clear avatar and emotion-log retention disclosures, retention limits, and deletion controls before enabling the skill.

Risk: Emoji generation may send avatar-derived inputs to Qwen/DashScope through an external image generation dependency.

Mitigation: Require explicit third-party processing disclosure, user consent where needed, and controlled API configuration before generation is allowed.

Risk: Local file paths and version cleanup depend on user or channel identifiers.

Mitigation: Restrict allowed channels and users, validate path-derived identifiers, and review version cleanup behavior before deployment.

Risk: Security evidence flags hidden user/channel gating and a suspicious verdict.

Mitigation: Install only in trusted deployment environments after reviewing allowed channels, user gating, and operational controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wdkmail/skills/local-auto-emoji)
- [Artifact skill manifest](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Chat text and MEDIA path directives, with generated PNG emoji files and JSON configuration/state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Qwen/DashScope image generation and retain avatar-derived local assets; review controls before enabling.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
