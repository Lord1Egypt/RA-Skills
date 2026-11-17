## Description:

Converts a specific video-material JSON format with oralBroadcastingList, materialList, and bgmInfo into a natural-language video production description for Jianying workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2719040953](https://clawhub.ai/user/2719040953)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video workflow builders use this skill to convert structured media JSON into Jianying-ready video instructions with timeline, subtitle, material, background image, BGM, and special-request details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated descriptions may expose raw media URLs from trusted input JSON.

Mitigation: Use trusted input, avoid publishing raw media links unless authorized, and prefer HTTPS with proper URL encoding or signed links in downstream workflows.

## Reference(s):

- [JSON Format Reference](references/json-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/2719040953/skills/json-to-jianying-description)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style natural-language video description]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calculated timestamps, subtitle ranges, material keys or URLs, background image, BGM details, and requested effects.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
