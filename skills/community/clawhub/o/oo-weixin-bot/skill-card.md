## Description:

Operate Weixin Bot to read updates, download media, and send text or media through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read Weixin Bot updates, download media, and send text or media through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloading media decrypts attachments and uploads them to file transit, which can expose private files.

Mitigation: Require confirmation before each upload and establish who can access file transit and how long files are retained; use a verified CLI release and review automatic skill synchronization.

## Reference(s):

- [Weixin Bot homepage and API documentation](https://github.com/Tencent/openclaw-weixin)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, API responses, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include message text or downloaded media; sending messages and media changes conversation state.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
