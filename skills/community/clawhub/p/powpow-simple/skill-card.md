## Description:

帮助用户把旅行照片和素材整理成帖子发布到 PowPow，或创建并发布带有公开地图位置的可聊天数字人。

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

适合想在 PowPow 分享旅行内容，或创建并发布可聊天数字人的用户。技能帮助用户准备帖子内容、选择图片和地点，并在用户明确确认后完成发布流程。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published text, photos, and a location can be shared on a public map.

Mitigation: Review the account, photos, text, and location before publishing; omit the location if you do not want a map pin.

Risk: Creating a digital human spends two non-refundable badges and expires after 30 days.

Mitigation: Confirm the badge cost and expiry before creating it.

Risk: A user may not understand the Chinese preview before publishing.

Mitigation: Request a translation of the preview before confirming publication.

Risk: The companion CLI performs login and network operations.

Mitigation: Review the separate powpow-cli package before installing it, and enter the password only in the user's own terminal.

## Reference(s):

- [PowPow official site](https://global.powpow.online)
- [PowPow public map](https://global.powpow.online/map)
- [About PowPow video](https://www.bilibili.com/video/BV1Wu826UEVz/)
- [Security guidance](references/security.md)
- [Product screenshots guide](references/screenshots.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Chinese conversational guidance and Markdown post previews, with companion CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts may include text, images, a location, and a digital-human tag; publishing and digital-human creation require the user's explicit confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
