## Description:

Gigma AI Design Canvas helps agents create, edit, preview, and export social media graphics, thumbnails, banners, cards, and batch designs on a cloud-hosted editable canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through creating editable visual designs, arranging canvas elements, previewing layouts, and exporting PNG assets. It is suited for social media posts, thumbnails, banners, cards, and repeated design variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design content is handled through a third-party cloud design service.

Mitigation: Install and use the skill only when third-party cloud processing is acceptable for the intended design content.

Risk: Exported PNG assets are hosted externally behind signed URLs for 7 days.

Mitigation: Do not export confidential, proprietary, or sensitive designs unless that external hosting behavior is acceptable.

Risk: Imported image assets must be reachable through public HTTPS URLs.

Mitigation: Use approved public assets or approved hosting locations for imported images.

## Reference(s):

- [Gigma documentation](https://gigma-doc.10xboost.org)
- [Gigma web app](https://gigma.10xboost.org)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/gigma-design)

## Skill Output:

**Output Type(s):** [guidance, configuration, text, markdown]

**Output Format:** [Markdown guidance with MCP configuration steps and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents toward screenshot previews, exported PNG files, and signed export URLs when used with the Gigma cloud service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
