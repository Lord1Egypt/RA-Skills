## Description:

Helps OpenClaw users set up Gokapi sharing, upload and send files through links, and revoke shared links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meska](https://clawhub.ai/user/meska)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users share files through their own Gokapi instance, choose retention and download limits, deliver links to intended recipients, or revoke existing links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared link could expose a private file to unintended recipients or remain accessible longer than intended.

Mitigation: Confirm the file, recipient, retention period, and optional download limit before upload; send the link only to the intended recipient and revoke it when needed.

Risk: A compromised Gokapi instance or overprivileged API key could expose shared files or allow unauthorized actions.

Mitigation: Use a trusted HTTPS instance, scope the key to necessary permissions, restrict key access to that instance, and keep the key out of chat.

Risk: Standard API uploads do not provide end-to-end encryption.

Mitigation: Use Gokapi's encrypted client workflow if end-to-end encryption is required.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/meska/skills/gokapi-file-sharing)
- [First-use setup](artifact/references/setup.md)
- [API upload and link management](artifact/references/api-upload.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown with download links and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports retention and download limits; distinguishes upload from delivery and confirms revocation.]

## Skill Version(s):

1.0.5 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
