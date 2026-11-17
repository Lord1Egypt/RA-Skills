## Description:

Removes image backgrounds with Bria RMBG 2.0 to produce transparent PNG cutouts and foreground masks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galbria](https://clawhub.ai/user/galbria)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and content operations teams use this skill to remove backgrounds from product photos, portraits, and other images for e-commerce, compositing, catalogs, and asset pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are sent to Bria's API for processing.

Mitigation: Install and use only when external processing by Bria is acceptable for the images being handled.

Risk: The helper caches Bria credentials locally.

Mitigation: Protect or avoid plaintext token storage and review local credential handling before deployment.

Risk: The helper can send API keys and image data to configured API origins and polling URLs.

Mitigation: Restrict the helper to the remove-background endpoint, pin allowed API origins, and validate polling URLs before production use.

Risk: Temporary payload files may contain encoded image data during API calls.

Mitigation: Use secure temporary-file handling and remove temporary payloads promptly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/galbria/skills/image-remove-background)
- [API Endpoints Reference](references/api-endpoints.md)
- [Shell Client](references/code-examples/bria_client.sh)
- [Bria AI](https://bria.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated transparent PNG result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce shell commands that authenticate with Bria, call the remove-background API, poll async jobs, and download PNG outputs.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
