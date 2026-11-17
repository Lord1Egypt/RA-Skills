## Description:

Helps an agent search M-Team for media torrents, present ranked results to the user, and send the selected torrent to a local Transmission instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengqijun](https://clawhub.ai/user/dengqijun)

### License/Terms of Use:

MIT-0

## Use Case:

Personal media-server users and developers use this skill to search M-Team by natural-language request, compare torrent options, and add a confirmed selection to Transmission with an appropriate NAS save path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start local torrent downloads through Transmission.

Mitigation: Require a clear user confirmation before adding any torrent and verify that M-Team and torrent usage complies with applicable legal, privacy, and network policies.

Risk: Credentials and service endpoints are handled too loosely for automatic installation.

Mitigation: Use environment variables or a secret manager, avoid editing secrets into source, and use a least-privileged Transmission account.

Risk: Remote download URLs and torrent payloads are fetched before being sent to Transmission.

Mitigation: Validate the returned download URL and torrent content before fetching or adding it.

Risk: The artifact frames proxy headers and Cloudflare bypass behavior as part of operation.

Mitigation: Remove or replace the Cloudflare bypass framing and confirm proxy behavior against local network policy before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dengqijun/skills/mteam-transmission0-1)
- [Publisher Profile](https://clawhub.ai/user/dengqijun)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown resource lists and plain-text download status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes torrent title, size, seeder count, category, Chinese subtitle markers, and final Transmission save path; torrent IDs should remain internal to tool use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
