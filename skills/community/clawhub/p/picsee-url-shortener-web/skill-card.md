## Description:

Shorten URLs and optionally generate QR codes through PicSee (picsee.io), with logged-in access to analytics and history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picseeinc](https://clawhub.ai/user/picseeinc)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to shorten long links with PicSee, return the shortened URL, and optionally generate a QR code when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs submitted for shortening are sent to PicSee.

Mitigation: Use only links that are appropriate to share with PicSee; avoid internal, private, authenticated, or tokenized URLs.

Risk: Optional QR code generation installs unpinned Python packages into a persistent local virtual environment.

Mitigation: Review before use; prefer pinned dependencies with hashes or a constrained built-in QR generator.

## Reference(s):

- [PicSee web app](https://picsee.io/?url=)
- [ClawHub skill page](https://clawhub.ai/picseeinc/skills/picsee-url-shortener-web)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown response with a short URL and optional QR image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional QR generation creates /tmp/picsee_qr.png only after explicit user request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
