## Description:

Generates Gumroad product cover and preview images from customizable HTML templates, then captures PNG screenshots with Edge headless.

This skill is ready for commercial/non-commercial use.

## Publisher:

[careytian-ai](https://clawhub.ai/user/careytian-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to create, update, or batch-generate Gumroad product cover, preview, and thumbnail images from product information and predefined visual themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The screenshot workflow starts an unpinned local HTTP server with permissive CORS.

Mitigation: Use a pinned or already-installed local server, bind it to 127.0.0.1, serve only the generated image directory, remove CORS unless required, and stop the server after capture.

Risk: Generated marketing images can become inaccurate if they include prices or free-offer language that later changes.

Mitigation: Keep price and free-offer text out of generated images, matching the artifact workflow's image content rule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/careytian-ai/skills/gumroad-product-images)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTML templates and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for 600x600 cover images and 1280x720 preview images; generated artifacts are expected to be local HTML and PNG files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
