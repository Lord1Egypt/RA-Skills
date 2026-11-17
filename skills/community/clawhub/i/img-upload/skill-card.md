## Description:

Uploads a local image file to the img.scdn.io public image host and returns shareable public links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[big-dust](https://clawhub.ai/user/big-dust)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to turn a local image, screenshot, or generated image into a public URL for sharing, embedding in documents, or referencing from web content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files are uploaded to img.scdn.io and become publicly accessible.

Mitigation: Use only for non-sensitive images that the user explicitly wants hosted publicly.

Risk: Broad triggers and weak file validation can lead to unintended local file exposure.

Mitigation: Confirm the target file path and image content before upload, and avoid screenshots, documents, credentials, internal work, or private images unless reviewed first.

Risk: The returned delete URL can control removal of the hosted image.

Mitigation: Treat the delete URL as sensitive and avoid publishing it with the public image URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/big-dust/skills/img-upload)
- [Publisher profile](https://clawhub.ai/user/big-dust)
- [img.scdn.io upload API endpoint](https://img.scdn.io/api/v1.php)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and command output containing a public image URL and, when returned by the service, a delete URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The delete URL is sensitive control information and should not be shared casually.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
