## Description:

Remove image watermarks with the Nowatermark.info API, request polling, request_id resume, and public image URL validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxcoder11](https://clawhub.ai/user/maxcoder11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit authorized public image URLs for watermark removal, poll job status, and resume prior cleanup jobs by request_id.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can disclose the API key and submitted image URL if --base-url is pointed at an untrusted endpoint.

Mitigation: Use the default Nowatermark.info endpoint unless the alternate endpoint is fully controlled and trusted.

Risk: The service receives the submitted public image URL for processing.

Mitigation: Use only public, non-sensitive image URLs that the user is authorized to edit.

Risk: Watermark removal can be misused on images without sufficient rights.

Mitigation: Confirm authorization before submitting an image when ownership or permission is unclear.

## Reference(s):

- [Image Watermark API Reference](references/api.md)
- [Setup](setup.md)
- [Nowatermark.info](https://nowatermark.info)
- [ClawHub Skill Page](https://clawhub.ai/maxcoder11/skills/image-watermark-remover)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOWATERMARK_API_KEY and a direct public image URL; returns a cleaned image URL or failure details.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
