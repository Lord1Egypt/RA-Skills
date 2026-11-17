## Description:

Guides an agent through user-approved photo editing in PhotoFresco, including layers, adjustments, masks, previews, and image export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puma10](https://clawhub.ai/user/puma10)

### License/Terms of Use:

MIT-0

## Use Case:

People and creative teams use this skill to direct an agent to edit, review, and export images in PhotoFresco while approving the connection and permissions themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An untrusted or changing local editor server could access granted images.

Mitigation: Install only the pinned PhotoFresco server or a source checkout you trust, and grant only the needed read and write folders.

Risk: Exports can replace files, and previews or exports may disclose private image content.

Mitigation: Avoid overwrite unless replacement is intended, and review image sensitivity before requesting previews or exports.

Risk: Optional cloud or paid AI operations may send image content to external providers and incur charges.

Mitigation: Request cloud access and a spending budget only when the user specifically wants those features.

## Reference(s):

- [PhotoFresco website](https://photofresco.com/)
- [PhotoFresco workflows](references/workflows.md)
- [PhotoFresco troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PhotoFresco tools can produce image previews and PNG, PSD, or native image exports with user-granted access.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
