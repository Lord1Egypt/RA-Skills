## Description:

Gigma Design Canvas lets agents create, edit, preview, and export canvas-based graphics through Gigma MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, marketers, and external users can use this skill to create and revise social media graphics, thumbnails, banners, cards, and batch design variations through agent-controlled canvas operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP URL contains an embedded token that can grant broad create, edit, delete, preview, and export access to Gigma projects if exposed.

Mitigation: Treat the full MCP URL as a secret, avoid sharing configs or screenshots that include it, and regenerate the link immediately if exposure is suspected.

Risk: Design operations, exports, and provided image URLs are processed by the Gigma cloud service.

Mitigation: Use the skill only for projects and image sources that are appropriate to process through the connected third-party cloud service.

## Reference(s):

- [Gigma Documentation](https://gigma-doc.10xboost.org)
- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/skills/gigma-design-canvas)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Files, Configuration instructions]

**Output Format:** [Markdown guidance with MCP tool call examples, screenshot previews, and PNG export URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG exports may be generated at 1x, 2x, or 3x scale with signed URLs valid for 7 days.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
