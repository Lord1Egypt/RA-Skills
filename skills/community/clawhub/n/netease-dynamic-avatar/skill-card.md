## Description:

Guides users through converting and uploading an animated GIF or WebP as a NetEase Cloud Music web avatar, then verifying that its animation frames were preserved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuan-dev39](https://clawhub.ai/user/yuan-dev39)

### License/Terms of Use:

MIT

## Use Case:

External users can set an animated GIF or WebP as their own NetEase Cloud Music web avatar. Developers can follow the included conversion, upload, and verification steps to preserve animation frames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local uploader can send the image and temporary upload token over an unencrypted connection.

Mitigation: Require HTTPS for upload destinations and redirects before using the local uploader; keep temporary tokens out of shell history, repositories, and screenshots.

Risk: Remote one-line installers may change before they are run.

Mitigation: Prefer a reviewed, pinned package over remote installer commands.

Risk: The browser workflow changes the avatar on the logged-in NetEase account and publishes the selected image.

Mitigation: Run it only on your own account or an account you are authorized to manage, and use an image you intend to publish.

## Reference(s):

- [Protocol and reverse engineering notes](references/protocol.md)
- [NetEase Cloud Music](https://music.163.com)
- [ClawHub skill page](https://clawhub.ai/yuan-dev39/skills/netease-dynamic-avatar)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance with Python, JavaScript, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes steps for producing an animated WebP and verifying its frame data.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
