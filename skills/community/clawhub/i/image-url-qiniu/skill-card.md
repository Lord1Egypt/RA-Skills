## Description:

Download an image from a user-supplied HTTP(S) URL and upload it to Qiniu cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lubin1127](https://clawhub.ai/user/lubin1127)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to mirror a user-provided public image URL into Qiniu object storage and return a stable public media URL for backup, CDN delivery, or sharing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-supplied URLs and publish the fetched image to Qiniu without blocking internal network targets.

Mitigation: Run it only where egress is restricted to public internet destinations and block localhost, private-network, link-local, and cloud metadata addresses before execution.

Risk: Qiniu credentials could allow uploads outside the intended operational scope if broadly provisioned.

Mitigation: Use narrowly scoped credentials limited to the intended bucket or prefix and rotate them according to local policy.

Risk: Disabling SSL verification weakens transport authenticity checks.

Mitigation: Avoid the SSL bypass except under controlled administrative conditions.

## Reference(s):

- [Qiniu Cloud](https://www.qiniu.com/)
- [ClawHub skill page: image-url-qiniu](https://clawhub.ai/lubin1127/skills/image-url-qiniu)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text MEDIA_URL line with setup guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Qiniu credentials, a public-read bucket, uv, and a user-supplied HTTP(S) image URL.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
