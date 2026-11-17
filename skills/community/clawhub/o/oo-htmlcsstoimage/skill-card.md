## Description:

HTML/CSS to Image (htmlcsstoimage.com). Use this skill for ANY HTML/CSS to Image request — reading, creating, updating, and deleting data. Whenever a task involves HTML/CSS to Image, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use the connected HTML/CSS to Image service to create images from HTML/CSS or public webpage URLs, retrieve usage information, and manage generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded scripts that have not been audited, and startup synchronization may make broader changes to other agent skills.

Mitigation: Use a reviewed, pinned CLI installation. Set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization if broader agent changes are unwanted.

Risk: Submitted HTML/CSS is processed through OOMOL, and image creation or deletion changes service data.

Mitigation: Consider whether submitted content is suitable for processing and retain the required approval steps for image creation and deletion.

## Reference(s):

- [HTML/CSS to Image skill listing](https://clawhub.ai/oomol/skills/oo-htmlcsstoimage)
- [HTML/CSS to Image documentation](https://docs.htmlcsstoimage.com/)
- [HTML/CSS to Image homepage](https://htmlcsstoimage.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Image assets, JSON, Shell commands]

**Output Format:** [JSON action payloads and responses, plus generated image assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch image creation supports up to 25 images per request.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
