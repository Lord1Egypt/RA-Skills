## Description:

Search Google Images with FlashData for image URLs, source pages, dimensions and titles. Use to find visual references, diagrams, product images or images that meet a size requirement. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can search for visual references, diagrams, and product images, then review image URLs, source pages, titles, and available dimensions. Use a FlashData API key with access to Google Images; queries spend paid FlashData Credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the hosted image search requires a FlashData API key and incurs paid query costs; scan coverage was partial and two local path-like references could not be resolved.

Mitigation: Keep the key in protected environment configuration, review the unresolved references before installation, and check pricing or a quote before running paid queries.

## Reference(s):

- [FlashData Google Images documentation](https://flashdata.dev/docs/sources/google_images?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_images-task)
- [FlashData MCP](https://flashdata.dev/mcp?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_images-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_images-task)
- [references/query.json](artifact/references/query.json)
- [references/schema.json](artifact/references/schema.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Image search result metadata, presented as structured JSON or a text/Markdown list or table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns image URLs and available titles, dimensions, and source-page links; it does not download image files. Result counts may vary.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
